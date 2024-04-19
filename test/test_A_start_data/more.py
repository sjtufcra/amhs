import oracledb
import threading
import concurrent.futures
import logging
from contextlib import contextmanager
# 假设已有一个线程安全的数据库连接池
class OracleConnectionPool:
    def __init__(self, dsn, user, password, max_connections=5):
        self.dsn = dsn
        self.user = user
        self.password = password
        self.max_connections = max_connections
        self.connections = []
        self.lock = threading.Lock()

    @contextmanager
    def get_connection(self):
        with self.lock:
            while len(self.connections) < self.max_connections:
                conn = oracledb.connect(user=self.user, password=self.password, dsn=self.dsn)
                self.connections.append(conn)
            conn = self.connections.pop(0)
        try:
            yield conn
        finally:
            with self.lock:
                self.connections.append(conn)

    def release_connection(self, conn):
        pass  # Not needed for this example, as connections are managed by the context manager


db_pool = OracleConnectionPool("your_dsn", "your_user", "your_password")

def process_order_threaded(p, order_key, order_value):
    with db_pool.get_connection() as db_conn:
        cursor = db_conn.cursor()

        # Perform database write operations using the cursor
        # Example: Insert a new order into an "orders" table
        cursor.execute("""
            INSERT INTO orders (order_key, order_value)
            VALUES (:order_key, :order_value)
        """, {"order_key": order_key, "order_value": str(order_value)})

        # Commit changes
        db_conn.commit()

        cursor.close()

def task_assign_new(p):
    g, max_g = 1, 6

    while p.runBool:
        log.info(f'run status: {p.runBool}')

        # Refresh vehicles, tasks, and map info
        p = vehicle_load(p)
        p = read_instructions(p)
        p.map_info = revise_map_info(p)

        # Refresh before assigning
        p.used_vehicle = set()
        j, n = 0, 0
        car = 0

        # Process orders in parallel using a thread pool
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {
                executor.submit(
                    process_order_threaded,
                    p,
                    k,
                    v,
                ): k
                for k, v in p.orders.items() if v.finished == 0
            }

            for future in concurrent.futures.as_completed(futures):
                order_key = futures[future]
                try:
                    future.result()
                    n += 1
                    car += 1
                except Exception as exc:
                    log.error(f"Error processing order '{order_key}': {exc}")

        g += 1
        log.info(f'this is the car count in the mission batch:{g},{car}')
        log.info(f'this is the task count in the mission batch:{g},{n}')
        log.info(f'this is the task batch:{g}')

    return p
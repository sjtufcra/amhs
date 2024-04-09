function fetchR(url, method = 'GET', data = null) {
    const options = {
      method,
      headers: {
        'Content-Type': 'application/json',
      },
    };
  
    if (method !== 'GET' && data) {
      options.body = JSON.stringify(data);
    }
  
    return fetch(url, options)
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        return response.json();
      })
      .catch((error) => {
        console.error('Error fetching data:', error);
        throw error;
      });
  }
  
//   // 使用示例
//   fetchRequest('https://api.example.com/data')
//     .then((response) => {
//       console.log(response);
//     })
//     .catch((error) => {
//       console.error(error);
//     });

export default fetchR;
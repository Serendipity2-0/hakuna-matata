// Simple script to test the typing API
const fetch = require('node-fetch');

async function testApi() {
  try {
    // Test POST endpoint
    console.log('Testing POST endpoint...');
    const postResponse = await fetch('http://localhost:3000/api/typing', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        wpm: 75,
        accuracy: 90,
        testDuration: 60,
      }),
    });
    
    const postData = await postResponse.json();
    console.log('POST response:', postData);
    
    // Test GET endpoint
    console.log('\nTesting GET endpoint...');
    const getResponse = await fetch('http://localhost:3000/api/typing');
    const getData = await getResponse.json();
    console.log('GET response:', getData);
    
  } catch (error) {
    console.error('Error testing API:', error);
  }
}

testApi();

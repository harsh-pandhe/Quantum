const express = require('express');
const bodyParser = require('body-parser');
const app = express();
const port = 3000;

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

const { exec } = require('child_process');

app.get('/run-command', (req, res) => {
    exec('python app.py', (error, stdout, stderr) => {
        if (error) {
            console.error(`Error executing command: ${error.message}`);
            return res.status(500).json({
                message: 'Error executing command',
                error: error.message,
                stderr: stderr
            });
        }
        if (stderr) {
            console.error(`stderr: ${stderr}`);
            return res.status(500).json({
                message: 'Error in command execution (stderr present)',
                stderr: stderr
            });
        }
        res.json({
            message: 'Command executed successfully',
            output: stdout
        });
    })
});


app.get('/', (req, res) => {
    res.send('Hello World!');
});


app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});
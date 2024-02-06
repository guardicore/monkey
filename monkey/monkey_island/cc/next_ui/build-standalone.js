// eslint-disable-next-line @typescript-eslint/no-var-requires
const { exec } = require('child_process');
// eslint-disable-next-line @typescript-eslint/no-var-requires
const fs = require('fs');
// eslint-disable-next-line @typescript-eslint/no-var-requires
const path = require('path');

const serverFilePath = './server-prod.js';
const serverCommonPath = './server-common.js';
const serverConfigPath = './generated-next-config.js';
const staticDirPath = '.next/static';

const standaloneDirPath = '.next/standalone';

function moveFile(filePath, destinationDir) {
    const fileName = path.basename(filePath);
    const destPath = path.join(destinationDir, fileName);
    fs.cp(filePath, destPath, (err) => {
        if (err) {
            console.error(`Error moving file ${fileName}:`, err);
            throw err;
        } else {
            console.log(`Moved file ${fileName} to ${destPath}`);
        }
    });
}

async function prepareStandaloneDir() {
    try {
        moveFile(serverFilePath, standaloneDirPath);
        moveFile(serverCommonPath, standaloneDirPath);
        moveFile(serverConfigPath, standaloneDirPath);

        const staticInStandaloneDirPath = path.join(
            standaloneDirPath,
            '.next/static'
        );
        fs.cp(
            staticDirPath,
            staticInStandaloneDirPath,
            { recursive: true },
            (err) => {
                if (err) {
                    console.error(`Error moving static dir:`, err);
                    throw err;
                } else {
                    console.log(
                        `Moved static dir to ${staticInStandaloneDirPath}`
                    );
                }
            }
        );
    } catch (err) {
        console.error('Error preparing standalone dir:', err);
    }
}

exec('next build', (error, stdout, stderr) => {
    if (error) {
        console.error(`Error during build: ${error.message}`);
        throw error;
    }
    if (stderr) {
        console.error(`Build error/warning: ${stderr}`);
        throw new Error(`Build error/warning: ${stderr}`);
    }
    console.log('Build successful:', stdout);
    prepareStandaloneDir();
    console.log('Build complete.');
});

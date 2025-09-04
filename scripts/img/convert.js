import { readdirSync } from 'fs';
import path from 'path';
import sharp from 'sharp';
import yargs from 'yargs';
import { hideBin } from 'yargs/helpers';

const argv = yargs(hideBin(process.argv))
	.option('input', {
		alias: 'i',
		type: 'array',
		description: 'Formats to create from',
		default: ['png']
	})
	.option('output', {
		alias: 'o',
		type: 'array',
		description: 'Formats to create',
		default: ['avif', 'webp']
	})
	.option('directory', {
		alias: 'd',
		type: 'string',
		description: 'Base directory to run in',
		default: './static/images'
	})
	.option('recursive', {
		alias: 'r',
		type: 'boolean',
		description: 'Run recursively on subdirectories?',
		default: true
	})
	.parse();

const loopThroughFolders = (startingDir) => {
	readdirSync(startingDir, { withFileTypes: true })
		.filter(
			(dirent) =>
				dirent.name[0] !== '.' && // don't run over hidden files
				((dirent.isDirectory() && argv.recursive) ||
					path.extname(dirent.name).toLowerCase() === '.png') // only run over png and directories
		)
		.map((dirent) => {
			const name = `${startingDir}/${dirent.name}`;

			// recursive loop if is directory
			if (dirent.isDirectory() && argv.recursive) loopThroughFolders(name);
			// otherwise create next gen images based on png
			else {
				const strippedName = name.replace('.png', '');
				const filename = strippedName.replace(argv.directory, '');
				for (let format of argv.output) {
					// create new next-gen files
					sharp(name)
						.toFormat(format)
						.toFile(`${strippedName}.${format}`, (err) => {
							if (err) console.log(err);
							else console.log(`--\x1b[32m ${filename}.${format}\x1b[0m`);
						});
				}
			}
		});
};

// start at the passed argument
loopThroughFolders(argv.directory);

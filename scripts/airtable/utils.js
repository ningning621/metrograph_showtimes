import Airtable from 'airtable';
import chalk from 'chalk';
import { createWriteStream, existsSync, mkdirSync, writeFile } from 'fs';
import slugify from 'slugify';
import { Readable } from 'stream';
import { finished } from 'stream/promises';

import 'dotenv/config';

/**
 * @typedef {import('airtable').Base} AirtableBase
 * @typedef {import('airtable').Record} AirtableRecord
 */

/** @type {AirtableBase} Airtable base instance. */
export const airtable = new Airtable({ apiKey: process.env.AIRTABLE_PAT }).base(
	process.env.AIRTABLE_BASE_ID
);

/**
 *
 * @param {{ url: string; id: string; }} Image - the image object from airtable
 * @param {'' | 'resources' | 'examples'} groupDir - the group directory to store the image in. if empty, left it root
 * @returns {string | undefined} - reference path for svelte enhanced:img
 */
export const download = async ({ url, id }, groupDir = '') => {
	if (!url || !id) return undefined;

	try {
		filename = slugify(id, { lower: true, remove: /[*+~()'"!:@]/g });

		if (groupDir) {
			const groupDirSlug = slugify(groupDir, { lower: true });
			filename = `${groupDirSlug}/${filename}`;

			// ensure the wrapping folder exists
			if (!existsSync(`./src/lib/assets/${groupDirSlug}`)) {
				mkdirSync(`./src/lib/assets/${groupDirSlug}`, { recursive: true });
			}
		}

		const path = `./src/lib/assets/${filename}`;
		const ref = filename;

		const res = await fetch(url);
		const fileStream = createWriteStream(path);
		await finished(Readable.fromWeb(res.body).pipe(fileStream));

		return ref;
	} catch (err) {
		console.error(err);
		return undefined;
	}
};

/**
 * turn an array of objects into an object of objects keyed by a field. Add a 'Status' field to split into staging and prod.
 * @param {unknown[]} records - records
 * @param {Function} key - field to key to
 */
export const keyBy = (records, key) => {
	if ('Status' in records[0]) {
		return {
			staging: Object.fromEntries(records.map((record) => [key(record), record])),
			prod: Object.fromEntries(
				records.filter((record) => record.Status === 'Live').map((record) => [key(record), record])
			)
		};
	}

	return Object.fromEntries(records.map((record) => [key(record), record]));
};
/**
 *
 * @param {string} str - a paragraph of possibly multiple paragraphs
 * @returns {string}
 */
export const formatGraf = (str) => {
	if (!str) return '';
	return str
		.split('\n\n')
		.map((d) => d.trim())
		.filter((d) => d)
		.join('\n\n');
};

/**
 * Split a string into an array of trimmed lines.
 * @param {string} strArr - The string to split.
 * @returns {string[]} The array of trimmed lines.
 */
export const splitlines = (strArr) =>
	strArr
		?.trim()
		?.split('\n')
		.map((d) => d.trim());

/**
 * Fetch associated records from Airtable.
 * @param {string[]} associated - The associated record IDs.
 * @param {string} table - The table name.
 * @returns {Promise<AirtableRecord[]>} The array of associated records.
 */
export const fetchAssociated = async (associated, table) => {
	if (!associated?.length || !table) return [];
	const records = await Promise.all(associated.map((d) => find(table, d)));
	return records;
};

/**
 * get our internal id from a base's airtable record id
 * @param {string[]} uuids - airtable's unique record id
 * @param {string} table - the table name or id
 * @param {string} key - the target column to derive our id from
 */
export const getIds = async (uuids, table, key) => {
	if (!uuids?.length || !key) return [];
	const ids = await Promise.all(
		uuids.map(async (uuid) => {
			if (!uuid) return undefined;
			const record = await find(table, uuid);
			return record?.[key];
		})
	)?.then((results) => results.filter((d) => d));

	return ids;
};

/**
 * Search for records in Airtable.
 * @param {string} query - The search query.
 * @param {string} base - The base name.
 * @param {string} view - The view name.
 * @param {(record: Record<string, unknown>[]) => void} [callback] - The callback function.
 * @returns {Promise<Record<string, unknown>[]>} The array of matching records.
 */
export const search = async (query, base, view, callback) => {
	return await airtable(base)
		?.select({ view, filterByFormula: query })
		?.all()
		?.then((records) => {
			const fields = records.map((record) => ({ ...record.fields, uuid: record.id }));
			if (callback) return callback(fields);
			return fields;
		});
};

/**
 * Select all records from Airtable.
 * @param {string} base - The base name.
 * @param {string} view - The view name.
 * @param {(record: Record<string, unknown>[]) => void} [callback] - The callback function.
 * @returns {Promise<Record<string, unknown>[]>} The array of all records.
 */
export const selectAll = async (base, view, callback) => {
	return await airtable(base)
		?.select({ view })
		?.all()
		?.then(async (records) => {
			const parsed = await Promise.all(
				records?.map(async (record) => {
					const fields = {
						...record.fields,
						uuid: record.id
					};

					// if there's an image field, download it
					if (fields?.Image?.[0]?.url) {
						try {
							fields.Image = await download(fields.Image, base);
						} catch (err) {
							console.error(err);
						}
					}

					return fields;
				})
			);

			if (callback) return await callback(parsed);

			return parsed;
		})
		.catch((err) => {
			console.error(err);
			return undefined;
		});
};

/**
 * Find a record in Airtable.
 * @param {string} base - The base name.
 * @param {string} id - The record ID.
 * @param {(record: Record<string, unknown>) => void} [callback] - The callback function.
 * @returns {Promise<Record<string, unknown>>} The found record.
 */
export const find = async (base, id, callback) => {
	return await airtable(base)
		?.find(id)
		?.then(async (record) => {
			const fields = { ...record.fields, uuid: record.id };

			if (callback) return await callback(fields);
			else return fields;
		})
		.catch((err) => {
			console.error(err);
			return undefined;
		});
};

/** FILE HANDLING */

/**
 *
 * @param {string} title - title of the data
 * @param {string} filepath - relative filepath to write to
 * @param {unknown} data - data to write
 * @returns {void}
 */
export const write = async (title, filepath, data) => {
	writeFile(filepath, JSON.stringify(data, null, 2), (err) => {
		if (err) {
			console.error(err);
			return;
		}

		console.log(
			chalk.green(
				`${chalk.bold(title)}: ${Array.isArray(data) ? data.length : Object.keys(data).length} records -> ${filepath}`
			)
		);
	});
};

/**
 * Write staging and prod data to files.
 * @param {string} title
 * @param {unknown} staging
 * @param {unknown} prod
 */
export const writeStagingProd = async (title, staging, prod) => {
	const filename = slugify(title, { lower: true });

	write(filename, `./src/lib/data/airtable/staging/${filename}.json`, staging);

	if (process.env.UPDATE_PROD_DATA && prod) {
		write(filename, `./src/lib/data/airtable/prod/${filename}.json`, prod);
	}
};

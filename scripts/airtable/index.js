import chalk from 'chalk';
import slugify from 'slugify';

import { getIds, keyBy, selectAll, write, writeStagingProd } from './utils.js';

import 'dotenv/config';

/** @typedef {string} BaseName The name of the base. */
/** @typedef {string} ViewName The name of the view in the base. */
/** @typedef {(records: Record<string, unknown>[]) => Record<string, unknown>} Callback The callback function, used to mutate data per-record as its grabbed. By default, we like to key things as Object of Objects (ex `{ uuid: { ...data } }`). This makes lookups on the front-end much easier */
/** @typedef {Record<string, unknown>} Rec The record fields object. */
/** @typedef {Record<string, Rec> || Rec[] } Records The array of all records. */
/** @typedef {Base} BaseName - The name of the base. */
/** @typedef {{ base: BaseName; view: ViewName; callback: Callback; data: Records; }} Base An array of object oriented to iterate over and grab all data files. */

/**
 * The array of bases to grab data from.
 * @type {Base[]}
 */
const bases = [
	{
		base: 'Example',
		view: 'All Records',
		callback: async (records) => {
			const parsed = await Promise.all(
				records.map(async (record) => ({
					...record,
					Assigned: await getIds(record.Assigned, 'People', 'Name')
				}))
			);
			const keyed = keyBy(parsed, (d) => d.ID);
			return keyed;
		},
		data: undefined
	},
	{
		base: 'People',
		view: 'All People',
		callback: (records) => keyBy(records, (d) => d.Name),
		data: undefined
	}
];

const getOptions = async () => {
	const base = await (
		await fetch(`https://api.airtable.com/v0/meta/bases/${process.env.AIRTABLE_BASE_ID}/tables`, {
			headers: { Authorization: `Bearer ${process.env.AIRTABLE_PAT}` }
		})
	).json();

	const options = Object.fromEntries(
		base.tables
			?.filter((table) => table?.fields.some((field) => field?.options?.choices))
			.map((table) => [
				table.name,
				Object.fromEntries(
					table.fields
						.filter((field) => field?.options?.choices)
						.map((field) => [field.name, field.options.choices.map((d) => d.name)])
				)
			])
	);

	// write all the options out
	return await write(
		'options',
		`./src/lib/data/airtable/${process.env.PUBLIC_DATA_VERSION === 'prod' ? 'prod' : 'staging'}/options.json`,
		options
	);
};

const main = async () => {
	// getOptions();

	// await all base data before mutating further
	await Promise.all(
		bases.map(async (d) => {
			const records = (await selectAll(d.base, d.view, d?.callback)) || [];

			if (!records) {
				console.log(chalk.yellow(`${d.base} - no records found in ${d.view} view`));
			}

			bases.find((b) => b.base === d.base).data = records;

			if (records.staging) {
				writeStagingProd(d.base, records.staging, records.prod);
			} else {
				const filename = slugify(d.base, { lower: true });
				const filepathCommon = `./src/lib/data/airtable/${filename}.json`;
				write(d.base, filepathCommon, records);
			}
		})
	);

	////////////////////////////////////////
	// Any post-processing goes here
};

main();

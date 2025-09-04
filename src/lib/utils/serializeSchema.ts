/**
 * @param {Object} schema - The JSON-LD schema to serialize
 * @see https://jsonld.com for data structuring
 * @returns A script tag including the formatted JSON-LD
 */
export default (schema: object) =>
	`<script type="application/ld+json">${JSON.stringify(schema)}</script>`;

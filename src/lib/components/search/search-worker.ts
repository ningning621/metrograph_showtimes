import { init, search, lookup } from './search';

addEventListener('message', async (event) => {
	const { type, payload } = event.data;

	switch (type) {
		case 'init': {
			const res = await fetch(`${payload?.origin || ''}/content.json`);
			const { blocks } = await res.json();
			init(blocks);

			postMessage({ type: 'ready', payload: {} });

			break;
		}

		case 'query': {
			const { query, type } = payload;
			const nodes = search(query, type);

			postMessage({
				type: 'results',
				payload: { nodes, query, type }
			});

			break;
		}

		case 'recents': {
			const nodes = payload.map(lookup).filter(Boolean);

			postMessage({
				type: 'recents',
				payload: nodes
			});

			break;
		}
	}
});

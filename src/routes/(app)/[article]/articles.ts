const articles = import.meta.glob('./*.yaml', { import: 'default', eager: true });

Object.entries(articles).forEach(([path, article]) => {
	const rekeyed = path.match(/\.\/(.+)\.yaml/)?.[1] || '';
	articles[rekeyed] = article;
	delete articles[path];
});

export default articles;

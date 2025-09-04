<script lang="ts">
	import { dev } from '$app/environment';
	import { page } from '$app/stores';
	import serializeSchema from '$lib/utils/serializeSchema';

	let {
		typekit,
		fontAwesome,
		googleFonts,
		url,
		siteName,
		title,
		tag,
		description,
		image,
		author,
		email,
		date_created,
		date_modified
	} = $derived($page.data as Metadata & Fontdata);

	let currentUrl = $derived(`${url}/${$page.url.pathname}`);
</script>

<svelte:head>
	<title>{!tag || title === tag ? title : `${title} • ${tag}`}</title>
	<meta name="robots" content="index,follow" />
	<meta
		itemprop="name"
		name="title"
		content={!tag || title === tag ? title : `${title} • ${tag}`}
	/>
	<meta name="author" content={author.name} />
	<meta itemprop="description" name="description" content={description} />
	<link itemprop="url" rel="canonical" href={currentUrl} />

	<!-- favicons in app.html -->
	<!-- https://evilmartians.com/chronicles/how-to-favicon-in-2021-six-files-that-fit-most-needs -->

	<!-- Open Graph / Facebook -->
	<meta property="og:type" content="article" />
	<meta property="og:url" content={currentUrl} />
	<meta property="og:title" content={title} />
	<meta property="og:site_name" content={siteName} />
	<meta property="og:description" content={description} />
	<meta itemprop="image" property="og:image" content={image.large.src} />
	<meta property="og:image:height" content={String(image.large.height)} />
	<meta property="og:image:width" content={String(image.large.width)} />
	<meta property="og:image:alt" content={image.alt} />

	<!-- Twitter -->
	<meta property="twitter:card" content="summary_large_image" />
	<meta property="twitter:site" content={author.twitter.handle} />
	<meta property="twitter:creator" content={author.twitter.handle} />
	<meta property="twitter:url" content={currentUrl} />
	<meta property="twitter:title" content={title} />
	<meta property="twitter:description" content={$page.data.description} />
	<meta property="twitter:image" content={image.small.src} />
	<meta property="twitter:image:alt" content={image.alt} />

	<!-- PWA: Web Manifest -->
	<link rel="manifest" href="{dev ? '' : url}/site.webmanifest" crossorigin="use-credentials" />

	<!-- JSON+LD Organization -->
	{@html serializeSchema({
		'@context': 'http://schema.org',
		'@type': 'Organization',
		'@id': `${url}#organization`,
		url: currentUrl,
		name: siteName,
		description: description,
		email: email,
		logo: {
			'@context': 'http://schema.org',
			'@type': 'ImageObject',
			url: `${url}/apple-icon-180x180.png`,
			height: 180,
			width: 180
		}
	})}

	{@html serializeSchema({
		'@context': 'http://schema.org',
		'@type': 'Article',
		datePublished: date_created,
		dateCreated: date_created,
		dateModified: date_modified,
		image: {
			'@context': 'http://schema.org',
			'@type': 'ImageObject',
			url: image.large.src,
			height: image.large.height,
			width: image.large.width,
			caption: image.alt
		},
		mainEntityOfPage: url,
		url: currentUrl,
		inLanguage: 'en',
		author: {
			'@context': 'http://schema.org',
			'@type': 'Organization',
			url: author.url,
			name: author.name
		},
		headline: title,
		description: description,
		publisher: { '@id': `${url}#organization` },
		copyrightHolder: { '@id': `${url}#organization` },
		sourceOrganization: { '@id': `${url}#organization` },
		isAccessibleForFree: true
	})}

	<!-- FONTS -->
	<!-- edit in /src/lib/site.yaml -->
	{#if typekit}
		<link rel="stylesheet" href="https://use.typekit.net/{typekit}.css" crossorigin="anonymous" />
	{/if}
	{#if fontAwesome}
		<script src="https://kit.fontawesome.com/{fontAwesome}.js" crossorigin="anonymous"></script>
	{/if}
	{#if googleFonts}
		<link rel="preconnect" href="https://fonts.gstatic.com" />
		<link
			href="https://fonts.googleapis.com/css2?{googleFonts
				.map((font) => {
					const family = font.family.replace(/\s+/g, '+');
					const variations = [
						...(font?.weights?.map((weight) => `0,${weight}`) || []),
						...(font?.italics?.map((weight) => `1,${weight}`) || [])
					].join(';');
					return `family=${family}:ital,wght@${variations}`;
				})
				.join('&')}&display=swap"
			rel="stylesheet"
			crossorigin="anonymous"
		/>
	{/if}
</svelte:head>

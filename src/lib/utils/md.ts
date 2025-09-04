import type StateInline from 'markdown-it/lib/rules_inline/state_inline';

import MarkdownIt from 'markdown-it';
import MarkdownItAnchor from 'markdown-it-anchor';
import MarkdownItAttrs from 'markdown-it-attrs';
import MarkdownItContainer from 'markdown-it-container';

/**
 * @description Parse and render markdown to html. Add two empty lines between grafs to separate
 *              tags.
 * @param {string} string - The markdown string to parse
 */
export default (string: string): string => `<div class="markdown">${md.render(string)}</div>`;

/**
 * @see
 * {@link https://github.com/markdown-it/markdown-it#init-with-presets-and-options|Markdown-it presets + options}
 */
const md = new MarkdownIt({
	html: true,
	breaks: true,
	linkify: true,
	typographer: true
}).disable(['backticks']);

/**
 * Custom implementation of markdown-it-bracketed-spans featuring typescript
 *
 * @param md - MarkdownIt instance
 * @see
 * {@link https://github.com/mb21/markdown-it-bracketed-spans/tree/master|markdown-it-bracketed-spans}
 */
const bracketedSpansPlugin = (md: MarkdownIt) => {
	const span = (state: StateInline) => {
		const max = state.posMax;

		/** opening state */
		if (state.src.charCodeAt(state.pos) !== 0x5b) return false;

		const labelStart = state.pos + 1;
		const labelEnd = state.md.helpers.parseLinkLabel(state, state.pos, true);

		/** no closing bracket detected */
		if (labelEnd < 0) return false;

		const pos = labelEnd + 1;

		if (pos >= max || state.src.charCodeAt(pos) !== 0x7b) return false;
		else {
			state.pos = labelStart;
			state.posMax = labelEnd;

			state.push('span_open', 'span', 1);
			state.md.inline.tokenize(state);
			state.push('span_close', 'span', -1);

			state.pos = pos;
			state.posMax = max;

			return true;
		}
	};

	md.inline.ruler.push('bracketed-spans', span);
};

/**
 * @description Render all links with target=_blank and rel="noreferrer noopener"
 * @see https://github.com/markdown-it/markdown-it/blob/master/docs/architecture.md#renderer
 */
// Remember old renderer, if overridden, or proxy to default renderer
const defaultRender =
	md.renderer.rules.link_open ||
	function (tokens, idx, options, env, self) {
		return self.renderToken(tokens, idx, options);
	};

// eslint-disable-next-line camelcase
md.renderer.rules.link_open = function (tokens, idx, options, env, self) {
	// If you are sure other plugins can't add `target` - drop check below
	const token = tokens[idx];
	token.attrs ??= [];

	const targetIndex = token.attrIndex('target');

	if (targetIndex < 0)
		token.attrPush(['target', '_blank']); // add new attribute
	else token.attrs[targetIndex][1] = '_blank'; // replace value of existing attr

	// If you are sure other plugins can't add `rel` - drop check below
	const relIndex = token.attrIndex('rel');

	if (relIndex < 0)
		tokens[idx].attrPush(['rel', 'noreferrer noopener']); // add new attribute
	else token.attrs[relIndex][1] = 'noreferrer noopener'; // replace value of existing attr

	// pass token to default renderer.
	return defaultRender(tokens, idx, options, env, self);
};

md.use(bracketedSpansPlugin)
	.use(MarkdownItAttrs)
	.use(MarkdownItContainer)
	.use(MarkdownItAnchor, { tabIndex: false });

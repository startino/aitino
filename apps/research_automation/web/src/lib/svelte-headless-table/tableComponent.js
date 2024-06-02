import { derived } from 'svelte/store';
import { derivedKeys } from 'svelte-subscribe';
import { finalizeAttributes, mergeAttributes } from './utils/attributes.js';
export class TableComponent {
	id;
	constructor({ id }) {
		this.id = id;
	}
	attrsForName = {};
	attrs() {
		return derived(Object.values(this.attrsForName), ($attrsArray) => {
			let $mergedAttrs = {};
			$attrsArray.forEach(($attrs) => {
				$mergedAttrs = mergeAttributes($mergedAttrs, $attrs);
			});
			return finalizeAttributes($mergedAttrs);
		});
	}
	propsForName = {};
	props() {
		return derivedKeys(this.propsForName);
	}
	state;
	injectState(state) {
		this.state = state;
	}
	applyHook(pluginName, hook) {
		if (hook.props !== undefined) {
			this.propsForName[pluginName] = hook.props;
		}
		if (hook.attrs !== undefined) {
			this.attrsForName[pluginName] = hook.attrs;
		}
	}
}

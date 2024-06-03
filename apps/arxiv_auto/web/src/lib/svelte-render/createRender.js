export class ComponentRenderConfig {
	component;
	props;
	constructor(component, props) {
		this.component = component;
		this.props = props;
	}
	eventHandlers = [];
	on(type, handler) {
		this.eventHandlers.push([type, handler]);
		return this;
	}
	children = [];
	slot(...children) {
		this.children = children;
		return this;
	}
}
export function createRender(component, props) {
	return new ComponentRenderConfig(component, props);
}

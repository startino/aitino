<script lang="ts">
	import { Handle, Position, type Connection, type HandleComponentProps } from '@xyflow/svelte';

	type $$Props = HandleComponentProps;
	export let id: $$Props['id'] = undefined;
	export let type: $$Props['type'];
</script>

<Handle {id} class="!h-5 !w-5 rounded-none border-none !bg-teal-500" {type} {...$$restProps} />

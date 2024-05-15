<script lang="ts">
	import * as Form from '$lib/components/ui/form';

	export let provider: string;
</script>

<form method="POST" action="?/authProvider&provider={provider}">
	<Form.Button variant="outline" class="w-full">
		<slot />
	</Form.Button>
</form>

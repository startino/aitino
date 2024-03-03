<script lang="ts">
	import { SvelteFlowProvider } from '@xyflow/svelte';
	import { Menu } from 'lucide-svelte';
	import { writable } from 'svelte/store';

	import { Button } from '$lib/components/ui/button';
	import * as Sheet from '$lib/components/ui/sheet';
	import { setContext } from '$lib/utils';
	import { Shell } from '$lib/components/layout/shell';
	import { SideNav } from '$lib/components/ui/side-nav';

	let menuOpen = false;

	import {
		Building,
		CircleUserRound,
		Dna,
		Globe,
		HelpCircle,
		LogOut,
		MessagesSquare,
		Paperclip,
		ReceiptText,
		UsersRound,
		Zap
	} from 'lucide-svelte';
	import type { ComponentType } from 'svelte';
	import type { Icon } from 'lucide-svelte';
	import { Logo } from '$lib/components/ui/logo';

	let navigations: {
		name: string;
		items: {
			name: string;
			href: string;
			icon: ComponentType<Icon>;
			current: boolean;
			pendingCount?: number;
		}[];
	}[] = [
		{
			name: '',
			items: [
				{
					name: 'Auto-build',
					href: '/app/auto-build',
					icon: Zap,
					current: false
				}
			]
		},
		{
			name: '',
			items: [
				{
					name: 'Sessions',
					href: '/app/sessions',
					icon: MessagesSquare,
					current: false
				},
				{
					name: 'Community',
					href: '/app/community',
					icon: Globe,
					current: false
				}
			]
		},
		{
			name: '',
			items: [
				{
					name: 'Crew Editor',
					href: '/app/editors/crew',
					icon: UsersRound,
					current: false
				},
				{ name: 'Agent Editor', href: '/app/editors/agent', icon: Dna, current: false }
			]
		},
		{
			name: '',
			items: [
				{
					name: 'Account',
					href: '/app/account',
					icon: CircleUserRound,
					current: false
				}
			]
		}
	];
	let bottomNavigation = [{ name: 'Logout', href: 'logout', icon: LogOut, current: false }];
</script>

<Shell class="h-screen">
	<svelte:fragment slot="sidebarLeft">
		<SideNav {navigations} {bottomNavigation} />
	</svelte:fragment>

	<slot />
</Shell>

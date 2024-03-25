<script lang="ts">
	import type { ActionData, PageData } from './$types';
	import { Button } from '$lib/components/ui/button';
	import * as Card from '$lib/components/ui/card';
	import { Label } from '$lib/components/ui/label';
	import { Input } from '$lib/components/ui/input';
	import { Github } from 'lucide-svelte';
	import * as Alert from '$lib/components/ui/alert';
	import * as Form from '$lib/components/ui/form';
	import { formSchema, type FormSchema } from '$lib/schema';
	import type { SuperValidated } from 'sveltekit-superforms';
	import { superForm } from 'sveltekit-superforms/client';
	import { toast } from 'svelte-sonner';
	import { enhance } from '$app/forms';

	export let form: ActionData;
	export let data: PageData;

	let isSubmittedSuccessfully = false;

	const {
		form: formRegister,
		errors,
		enhance: enhanceRegister
	} = superForm(data.registerForm, {
		validators: formSchema
	});

	async function checkError() {
		console.log(
			$errors.display_name,
			'form display name',
			$errors.password,
			'form password',
			$errors.email,
			'errors'
		);
		if (
			$errors.display_name !== undefined ||
			$errors.password !== undefined ||
			$errors.email !== undefined
		) {
			toast.error('Please fill the form correctly');
		} else {
			if (form?.error) {
			} else {
				isSubmittedSuccessfully = true;
			}
		}
	}

	let localErrorMessage = '';
	$: localErrorMessage = form?.error;

	async function chekcAutoReloadError() {
		console.log('top:', localErrorMessage);
		setTimeout(() => {
			checkError();
		}, 3000);

		console.log('Error from checkAutoReloadError:', localErrorMessage);
	}
</script>

{#if isSubmittedSuccessfully}
	<Card.Root>
		<Card.Header>
			<Card.Title class="text-2xl">Check Your Email</Card.Title>
		</Card.Header>
		<Card.Content class="text-center">
			<p>
				We've sent a confirmation email to you. Please check your inbox to complete the registration
				process.
			</p>
			<Button href="/login" class="mt-4">Go to Login</Button>
		</Card.Content>
	</Card.Root>
{:else}
	<Card.Root>
		<Card.Header>
			<Card.Title class="text-2xl">Create an account</Card.Title>
			<Card.Description>Enter your email below to create your account</Card.Description>
		</Card.Header>
		<Card.Content>
			<div class="space-y-4">
				<form method="POST" class=" grid w-full grid-cols-2 gap-6" use:enhance>
					<Button variant="outline" formaction="?/register&provider=github" type="submit">
						<Github class="mr-2 h-4 w-4" />
						GitHub
					</Button>
					<Button variant="outline" formaction="?/register&provider=google" type="submit">
						<svg
							xmlns="http://www.w3.org/2000/svg"
							viewBox="0 0 48 48"
							class="mr-2"
							width="18px"
							height="28px"
							><path
								fill="#FFC107"
								d="M43.611,20.083H42V20H24v8h11.303c-1.649,4.657-6.08,8-11.303,8c-6.627,0-12-5.373-12-12c0-6.627,5.373-12,12-12c3.059,0,5.842,1.154,7.961,3.039l5.657-5.657C34.046,6.053,29.268,4,24,4C12.955,4,4,12.955,4,24c0,11.045,8.955,20,20,20c11.045,0,20-8.955,20-20C44,22.659,43.862,21.35,43.611,20.083z"
							/><path
								fill="#FF3D00"
								d="M6.306,14.691l6.571,4.819C14.655,15.108,18.961,12,24,12c3.059,0,5.842,1.154,7.961,3.039l5.657-5.657C34.046,6.053,29.268,4,24,4C16.318,4,9.656,8.337,6.306,14.691z"
							/><path
								fill="#4CAF50"
								d="M24,44c5.166,0,9.86-1.977,13.409-5.192l-6.19-5.238C29.211,35.091,26.715,36,24,36c-5.202,0-9.619-3.317-11.283-7.946l-6.522,5.025C9.505,39.556,16.227,44,24,44z"
							/><path
								fill="#1976D2"
								d="M43.611,20.083H42V20H24v8h11.303c-0.792,2.237-2.231,4.166-4.087,5.571c0.001-0.001,0.002-0.001,0.003-0.002l6.19,5.238C36.971,39.205,44,34,44,24C44,22.659,43.862,21.35,43.611,20.083z"
							/></svg
						>
						Google
					</Button>
				</form>
				<!-- </div> -->
				<div class="relative">
					<div class="absolute inset-0 flex items-center">
						<span class="w-full border-t" />
					</div>
					<div class="relative flex justify-center text-xs uppercase">
						<span class="bg-card px-2 text-muted-foreground"> Or continue with </span>
					</div>
				</div>
				<form action="?/register" method="POST" class="space-y-4" use:enhance>
					<div class="grid gap-2">
						<Label for="username">Display Name</Label>
						<Input
							id="display_name"
							name="display_name"
							type="display_name"
							placeholder="Display name"
							bind:value={$formRegister.display_name}
							class="flex  h-9 w-full rounded-md border border-input bg-transparent px-3 py-6 text-sm shadow-sm ring-offset-0 transition-colors file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring focus-visible:ring-offset-0 disabled:cursor-not-allowed disabled:opacity-50"
						/>
						{#if $errors.display_name}
							<Alert.Root variant="destructive" class="border-none p-0">
								<Alert.Description>{$errors.display_name}</Alert.Description>
							</Alert.Root>
						{/if}
					</div>
					<div class="grid gap-2">
						<Label for="email">Email</Label>
						<Input
							id="email"
							type="email"
							name="email"
							placeholder="minilik@gmail.com"
							bind:value={$formRegister.email}
							class="flex  h-9 w-full rounded-md border border-input bg-transparent px-3 py-6 text-sm shadow-sm ring-offset-0 transition-colors file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring focus-visible:ring-offset-0 disabled:cursor-not-allowed disabled:opacity-50"
						/>
						{#if $errors.email}
							<Alert.Root variant="destructive" class="border-none p-0">
								<Alert.Description>{$errors.email}</Alert.Description>
							</Alert.Root>
						{/if}
					</div>
					<div class="grid gap-2">
						<Label for="password">Password</Label>
						<Input
							id="password"
							type="password"
							name="password"
							placeholder="********"
							bind:value={$formRegister.password}
							class="flex  h-9 w-full rounded-md border border-input bg-transparent px-3 py-6 text-sm shadow-sm ring-offset-0 transition-colors file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring focus-visible:ring-offset-0 disabled:cursor-not-allowed disabled:opacity-50"
						/>
						{#if $errors.password && $errors.password.length > 0}
							<Alert.Root variant="destructive" class="border-none p-0">
								<Alert.Description class="p-0">
									{#each $errors.password as error}
										<div>{error}</div>
									{/each}
								</Alert.Description>
							</Alert.Root>
						{/if}
					</div>
					{#if form?.error}
						<Alert.Root variant="destructive" class="border-none p-0">
							<Alert.Description>{form?.error}</Alert.Description>
						</Alert.Root>
					{/if}
					<Button
						class="w-full"
						type="submit"
						on:click={() => {
							if (!($errors.email || $errors.password || $errors.display_name)) {
								chekcAutoReloadError();
							}
						}}>Create account</Button
					>
				</form>
			</div>
		</Card.Content>
		<div class="flex w-full justify-end p-0">
			<Card.Footer>
				<p class="text-md block text-right text-foreground">
					Already have an account? <a
						href="/login"
						class="text-secondary underline hover:text-accent/75">Sign in</a
					>
				</p>
			</Card.Footer>
		</div></Card.Root
	>
{/if}

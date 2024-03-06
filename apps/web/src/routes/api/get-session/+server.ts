import { error, json } from '@sveltejs/kit';
import * as db from '$lib/server/db';
import type { Session } from '$lib/types/models';

// TODO: I couldn't call this action from +page.server.ts
// So I'm calling it from here. If possible, move it back as a named action.
export async function GET({url}) {
    const sessionId = url.searchParams.get("sessionId");
    if (!sessionId) throw error(400, "This session does not exist. Please reload the page.");
    const session: Session | null = await db.getSession(sessionId);
    return json({session});
}

/* Error log to help fix
Error: Cannot use relative URL (?/get-session?sessionId=77161923-d076-498b-8054-e0ec5e618bce) with global fetch — use `event.fetch` instead: https://kit.svelte.dev/docs/web-standards#fetch-apis
    at globalThis.fetch (file:///C:/Users/antop/Documents/Development/aitino/apps/web/node_modules/.pnpm/@sveltejs+kit@2.5.2_@sveltejs+vite-plugin-svelte@3.0.2_svelte@4.2.12_vite@5.1.4/node_modules/@sveltejs/kit/src/exports/vite/dev/index.js:44:10)
    at loadNewMessage (C:/Users/antop/Documents/Development/aitino/apps/web/src/routes/app/sessions/Chat.svelte:52:26)
    at Object.eval [as callback] (C:/Users/antop/Documents/Development/aitino/apps/web/src/routes/app/sessions/Chat.svelte:47:14)
    at C:\Users\antop\Documents\Development\aitino\apps\web\node_modules\.pnpm\@supabase+realtime-js@2.9.3\node_modules\@supabase\realtime-js\dist\main\RealtimeChannel.js:410:22
    at Array.map (<anonymous>)
    at RealtimeChannel._trigger (C:\Users\antop\Documents\Development\aitino\apps\web\node_modules\.pnpm\@supabase+realtime-js@2.9.3\node_modules\@supabase\realtime-js\dist\main\RealtimeChannel.js:395:16)      
    at C:\Users\antop\Documents\Development\aitino\apps\web\node_modules\.pnpm\@supabase+realtime-js@2.9.3\node_modules\@supabase\realtime-js\dist\main\RealtimeClient.js:347:47
    at Array.forEach (<anonymous>)
    at C:\Users\antop\Documents\Development\aitino\apps\web\node_modules\.pnpm\@supabase+realtime-js@2.9.3\node_modules\@supabase\realtime-js\dist\main\RealtimeClient.js:347:18
    at Serializer.decode (C:\Users\antop\Documents\Development\aitino\apps\web\node_modules\.pnpm\@supabase+realtime-js@2.9.3\node_modules\@supabase\realtime-js\dist\main\lib\serializer.js:14:20)

*/
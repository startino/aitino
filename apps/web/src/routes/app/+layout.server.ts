import { error, redirect } from "@sveltejs/kit";
import type {PageServerLoad, Actions} from "./$types";

export const load: PageServerLoad = async ( {locals:{ getSession }}) => {

    const session = await getSession();
	const profileId = session?.user?.id; // TODO: add checks

	if (!profileId) {
		throw redirect(307, "/");
	}
	
    return {
		session
	};
}

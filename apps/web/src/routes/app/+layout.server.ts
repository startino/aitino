import { error, redirect } from "@sveltejs/kit";
import type {PageServerLoad, Actions} from "./$types";

export const load: PageServerLoad = async ( {locals:{ getSession }}) => {
    // BEGIN TEMP FORCE PROFILE
	// const profileId = "edb9a148-a8fc-48bd-beb9-4bf5de602b78"; //cookies.get("profileId");
	// const expirationDate = new Date();
	// expirationDate.setMonth(expirationDate.getMonth() + 1);
	// cookies.set("profileId", profileId, {
	// 	path: "/",
	// 	httpOnly: true,
	// 	sameSite: "strict",
	// 	secure: process.env.NODE_ENV === "production",
	// 	expires: expirationDate
	// });
	// END TEMP FORCE PROFILE

    const session = await getSession();
	const profileId = session?.user?.id; // TODO: add checks

	if (!profileId) {
		throw redirect(307, "/");
	}
	
    
}

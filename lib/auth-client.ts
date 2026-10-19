import { createAuthClient } from "better-auth/react";
import { usernameClient } from "better-auth/client/plugins";


export const authClient = createAuthClient({
    baseURL: process.env.NEXT_PUBLIC_BETTER_AUTH_URL!,
    plugins: [usernameClient()],
});

export const {signIn, signUp, signOut, useSession} = authClient;

/**
 * Accounts are username + password. Better Auth still requires an email on every
 * user, so sign-up stores this placeholder: derived from the (lower-cased, hence
 * unique) username, under the reserved ".invalid" domain that can never receive mail.
 * Students never see or type it.
 */
export function placeholderEmail(username: string): string {
    return `${username.trim().toLowerCase()}@students.invalid`;
}

# Test Cases — KAN-2: Verify login feature

## Test Case Summary

| TC ID | Priority | Scenario | Environment | Status |
| --- | --- | --- | --- | --- |
| TC-01 | P2 | Successful login with valid account | Production | Draft |
| TC-02 | P2 | Invalid password | Production | Draft |
| TC-03 | P2 | Invalid username | Production | Draft |
| TC-04 | P2 | Empty username | Production | Draft |
| TC-05 | P2 | Empty password | Production | Draft |
| TC-06 | P2 | Locked or disabled account | Production | Draft |
| TC-07 | P2 | Session timeout / expired session | Production | Draft |
| TC-08 | P2 | Logout flow | Production | Draft |
| TC-09 | P2 | Browser back navigation after logout | Production | Draft |
| TC-10 | P2 | Basic accessibility validation | Production | Draft |

## TC-01: Successful login with valid account

- Objective: Verify that a valid user can log in successfully.
- Priority: P2
- Preconditions:
  - Application is available in Production.
  - A valid active account exists.
- Steps:
  1. Navigate to the login page.
  2. Enter a valid username and valid password.
  3. Click the login button.
- Expected result:
  - User is authenticated successfully.
  - User is redirected to the expected landing page or dashboard.
  - No validation errors are shown.
  - Session is created successfully.

## TC-02: Invalid password

- Objective: Verify invalid password handling.
- Priority: P2
- Preconditions:
  - A valid username is known.
  - The password entered is incorrect.
- Steps:
  1. Navigate to the login page.
  2. Enter a valid username and an incorrect password.
  3. Click the login button.
- Expected result:
  - Login is rejected.
  - User remains on the login page or is returned to the relevant entry state.
  - A clear error message is displayed.
  - No authenticated session is created.

## TC-03: Invalid username

- Objective: Verify invalid username handling.
- Priority: P2
- Preconditions:
  - An invalid username is known.
- Steps:
  1. Navigate to the login page.
  2. Enter an invalid username and a valid password.
  3. Click the login button.
- Expected result:
  - Login is rejected.
  - Appropriate validation or authentication error appears.
  - No session is created.

## TC-04: Empty username

- Objective: Verify required-field validation for username.
- Priority: P2
- Preconditions:
  - Login page is loaded.
- Steps:
  1. Leave the username field empty.
  2. Enter a valid password.
  3. Click the login button.
- Expected result:
  - Login is blocked.
  - A clear validation message indicating the username is required is displayed.
  - No authentication attempt is accepted.

## TC-05: Empty password

- Objective: Verify required-field validation for password.
- Priority: P2
- Preconditions:
  - Login page is loaded.
- Steps:
  1. Enter a valid username.
  2. Leave the password field empty.
  3. Click the login button.
- Expected result:
  - Login is blocked.
  - A clear validation message indicating the password is required is displayed.
  - No authentication attempt is accepted.

## TC-06: Locked or disabled account

- Objective: Verify access is denied for locked or disabled accounts.
- Priority: P2
- Preconditions:
  - A locked, inactive, or disabled account exists.
- Steps:
  1. Navigate to the login page.
  2. Enter the locked/disabled account credentials.
  3. Click the login button.
- Expected result:
  - Login is denied.
  - User is shown a clear access restriction or account status message.
  - No protected pages are accessible.

## TC-07: Session timeout / expired session

- Objective: Verify expired or timed-out sessions are handled correctly.
- Priority: P2
- Preconditions:
  - A valid logged-in session can be expired or timed out.
- Steps:
  1. Log in successfully.
  2. Allow the session to expire or simulate timeout.
  3. Attempt to access a protected page or refresh the page.
- Expected result:
  - User is redirected to the login page or prompted to sign in again.
  - Previously available protected content is no longer accessible without reauthentication.
  - A clear session-expired message is displayed if applicable.

## TC-08: Logout flow

- Objective: Verify users can sign out cleanly.
- Priority: P2
- Preconditions:
  - User is logged in.
- Steps:
  1. Click the logout or sign-out control.
  2. Confirm the action if a confirmation step exists.
- Expected result:
  - Session is terminated successfully.
  - User is redirected to the login page or logged-out state.
  - Protected pages require reauthentication.

## TC-09: Browser back navigation after logout

- Objective: Verify protected content is not accessible after logout.
- Priority: P2
- Preconditions:
  - User logged in previously.
- Steps:
  1. Log in successfully.
  2. Log out.
  3. Use the browser back button or attempt to revisit a protected page.
- Expected result:
  - User is not granted access to protected content without reauthentication.
  - Session state is invalidated correctly.
  - User is redirected to the login page or a safe logged-out state.

## TC-10: Basic accessibility validation

- Objective: Check that the login form is usable through keyboard and basic assistive technology expectations.
- Priority: P2
- Preconditions:
  - Login page is loaded.
- Steps:
  1. Use the keyboard only to navigate the login form.
  2. Tab through username, password, and login controls.
  3. Verify focus order and interactions.
  4. Confirm labels and instructions are present and understandable.
- Expected result:
  - Focus order is logical and visible.
  - Fields have clear labels.
  - The form can be used without a mouse.
  - Error messages are perceivable and actionable.

## Exit Criteria for Test Execution

- All P2 login scenarios above are executed in Production.
- No critical or high-severity issues remain unresolved for the login feature.
- Authentication and session-related behaviors match expected outcomes.
- Any defects found are recorded with reproduction steps and impact.

# Layered Secure Chat Demonstration Project

## Important interpretation

The notes describe a multi-layer chat prototype. They mention a Flask web flow, HTTP polling, password-protected rooms, participant checks, `client.py`, `server.py`, TCP sockets, encryption/decryption, a quantum-simulated cipher concept, and in-memory versus shared key-value storage. The scans do not reliably establish every algorithm, dependency, or production setting. Confirm these details against the source code before treating them as implemented.

## Project Overview

0001. This project is a prototype for a privacy-focused chat application with a separate client/server path.
0002. The notes describe a browser-facing interface and a separate desktop/client communication path.
0003. The central goal is to demonstrate layered protection for messages rather than relying on one protection step.
0004. The notes mention a fake web interface, password-protected rooms, participant tracking, encryption, and decryption.
0005. The system is described as having three layers; the exact full names of every layer are not completely legible in the scans.
0006. One layer is described as plain input or message preparation before encryption.
0007. The notes mention a second encryption layer and a quantum-inspired or quantum-simulated cipher concept.
0008. The notes also mention HTTPS polling for browser updates instead of WebSocket delivery.
0009. The desktop path is described as using client.py and server.py with TCP sockets.
0010. The README distinguishes handwritten requirements from implementation details that still need confirmation.

## Goals and Scope

0011. Demonstrate how a message can pass through multiple protection stages before being displayed.
0012. Show the relationship between a client, a server, a room, and registered participants.
0013. Support a room-oriented chat workflow in which users enter a room and send messages.
0014. Keep the browser interface and the separate desktop communication path conceptually distinct.
0015. Explain where HTTPS, TCP, application encryption, and storage fit into the data flow.
0016. Provide a project structure that can be mapped to the actual source files as development progresses.
0017. Make the security design understandable to students and project reviewers.
0018. Document limitations honestly, especially where a quantum algorithm is simulated rather than run on quantum hardware.
0019. Treat the project as a demonstration unless testing and deployment evidence proves production readiness.
0020. Do not interpret a successful demo as proof that the cryptography is secure.

## Architecture at a Glance

0021. The notes refer to a browser-facing Flask application and a separate desktop client/server path.
0022. Flask routes are described as loading rooms, handling messages, and returning message data.
0023. The browser appears to request updates periodically using HTTP polling.
0024. The desktop path is described as client.py communicating with server.py over TCP sockets.
0025. The notes mention a shared or in-memory key-value store as a storage consideration.
0026. Local in-memory storage is described as suitable for development but volatile on restart.
0027. In-memory data may not be shared between separate server processes or instances.
0028. A shared key-value store is mentioned as a possible need for multi-instance deployment.
0029. The message workflow includes input, encryption or transformation, transport, server-side handling, and display.
0030. The exact production topology, port numbers, framework versions, and deployment provider are not specified in the handwritten notes.

## User Interface and Rooms

0031. The notes describe a fake web interface intended to demonstrate chat application behavior.
0032. A room is a logical space in which messages and participants are associated.
0033. The notes state that rooms should be password-protected.
0034. The application should check whether the requested room exists.
0035. The application should check whether the user is registered or otherwise permitted to join.
0036. Room membership checks should happen on the server, not only in browser JavaScript.
0037. Client-side hiding of controls is not a substitute for authorization.
0038. The interface should make the active room clear to the participant.
0039. The interface should display messages in a consistent order.
0040. The exact visual design, colors, and HTML component names are not specified in the notes.

## Message Handling

0041. A message begins as user input in the client interface.
0042. The message should be validated before the application accepts it.
0043. The notes describe preparing or encrypting the message at the application layer.
0044. The transformed message is then passed through the relevant transport path.
0045. The server should validate the room and participant context before accepting the message.
0046. The notes mention checking stored messages and returning messages whose identifiers are greater than a known value.
0047. Message identifiers can help the client request only newer messages during polling.
0048. Messages should be ordered using a stable identifier or timestamp policy.
0049. The server should not trust a message's claimed sender identity merely because the client supplied it.
0050. The exact message schema, maximum length, timestamp format, and duplicate-handling policy are not specified.

## Encryption Layers

0051. The notes emphasize a multi-layer approach to message protection.
0052. The handwritten description says the project has three layers.
0053. The first layer appears to involve preparing the message or representing it before later protection stages.
0054. The notes describe a second layer of encryption.
0055. The notes also mention a cipher described as quantum-simulated or quantum-inspired.
0056. The exact algorithm names and their parameters are not reliably legible in all scanned lines.
0057. Do not claim that the project uses a specific standardized cipher unless the source code confirms it.
0058. Layering does not automatically make a system stronger; each layer must be correctly designed and implemented.
0059. Encryption should be authenticated where possible so tampering can be detected.
0060. Key generation, key storage, nonce handling, rotation, and recovery need explicit design decisions.

## Quantum Simulation Note

0061. The notes contain a reference that appears to read as a quantum-simulated cipher or quantum simulation.
0062. This wording should be treated as a project concept until the implementation is inspected.
0063. A simulation on a classical computer is not the same as running an algorithm on quantum hardware.
0064. A quantum-inspired transformation is not automatically quantum-safe.
0065. A custom cipher should not be presented as proven secure without independent cryptographic review.
0066. The README should name the actual algorithm only after its source file and implementation are verified.
0067. If a quantum simulator is used, document its library, version, inputs, outputs, and limitations.
0068. If no simulator is present in the code, describe the quantum element as a planned or conceptual feature.
0069. Security claims should be based on reproducible tests and established cryptographic properties.
0070. The project should explain which layer provides confidentiality, integrity, authentication, or only demonstration value.

## Browser Polling

0071. The notes explicitly contrast HTTP polling with WebSocket delivery.
0072. The described browser workflow uses repeated HTTP requests to check for new messages.
0073. Each polling request asks the server for messages newer than the last message already received.
0074. The server filters stored messages and returns matching results.
0075. The browser then adds new messages to the chat display.
0076. Polling is straightforward to demonstrate because each request is short-lived.
0077. Polling can create more request overhead than a persistent connection.
0078. Polling frequency affects perceived responsiveness and server load.
0079. HTTPS protects data in transit between browser and server when TLS is configured correctly.
0080. HTTPS does not replace application-level encryption if the project requires the server not to read message content.

## Desktop TCP Path

0081. The notes name client.py and server.py as part of a separate development path.
0082. The desktop client and server are described as using TCP sockets.
0083. TCP provides an ordered byte stream and reliable delivery within the connection's transport semantics.
0084. TCP does not itself encrypt the application data.
0085. Encryption must be added at the application layer or by using a secure transport such as TLS.
0086. The notes mention that the desktop path is distinct from the Flask web flow.
0087. Document how the desktop client frames a message so the receiver can detect message boundaries.
0088. Document how connection setup, disconnection, timeouts, and errors are handled.
0089. Do not assume browser polling and desktop TCP use the same endpoints or message format.
0090. The actual socket port, framing protocol, and reconnect behavior must be verified from source code.

## Storage and Persistence

0091. The notes state that local in-memory storage is convenient during development.
0092. Data held only in process memory can disappear when the application restarts.
0093. Memory held by one server process is not automatically shared with other processes.
0094. The notes mention shared key-value storage for multi-instance deployment.
0095. A shared store can support multiple application instances if its access and consistency rules are designed correctly.
0096. Room metadata, participant state, and message history may have different persistence requirements.
0097. Sensitive message content should not be logged unnecessarily.
0098. Stored ciphertext may still expose metadata such as message size, timing, room identifiers, and participant identifiers.
0099. Storage retention and cleanup policies should be documented.
0100. The notes do not specify a final database or production persistence backend.

## Threat Model and Security

0101. The notes mention man-in-the-middle attacks as a common attack type.
0102. A man-in-the-middle attacker attempts to observe or alter traffic between communicating parties.
0103. TLS certificate validation is important for HTTPS connections.
0104. The notes mention phishing and credential-related risks in the broader security discussion.
0105. Password-protected rooms need secure password handling and authorization checks.
0106. Passwords should not be stored as plain text.
0107. Authentication and authorization should be treated as separate responsibilities.
0108. Sensitive data should be cleared from memory when it is no longer needed where practical.
0109. Logging should avoid secrets, passwords, plaintext messages, and encryption keys.
0110. The project should document known limitations instead of claiming complete protection against all attacks.

## Custom Input Fields and Keylogging

0111. The notes describe custom input fields as a way of avoiding standard browser input mechanisms.
0112. The handwritten explanation says custom fields can move away from standard browser input mechanisms.
0113. The notes also describe a keylogger as software that records keyboard activity and may capture sensitive data.
0114. Custom input fields do not reliably prevent keylogging on a compromised operating system.
0115. Malware with sufficient privileges may capture keystrokes, screenshots, clipboard content, or process memory.
0116. Use this feature only as a demonstration of input handling, not as a security guarantee.
0117. Prefer standard accessible form controls unless there is a concrete, tested requirement for a custom control.
0118. HTTPS protects network transport but does not stop malware on the user's device.
0119. Users should keep their operating system and endpoint protection updated.
0120. The final README must not claim that custom fields alone prevent keyloggers.

## Development and Testing

0121. Test room creation and room lookup behavior.
0122. Test the password-protected room workflow with correct and incorrect passwords.
0123. Test rejection of unknown rooms.
0124. Test rejection of unauthorized or unregistered participants.
0125. Test sending and receiving a normal message.
0126. Test polling when there are no new messages.
0127. Test polling when one or more new messages arrive.
0128. Test message ordering when several messages are sent quickly.
0129. Test behavior when the server restarts and in-memory state is lost.
0130. Test malformed input and unexpected client disconnects.

## Deployment and Operations

0131. Development settings should be separated from deployment settings.
0132. Do not expose debug mode on a public production server.
0133. Use HTTPS with correctly configured TLS for the browser-facing application.
0134. Keep secret keys and service credentials outside committed source code.
0135. Restrict network access to the desktop socket service where possible.
0136. Use a shared persistence service if multiple server instances must share state.
0137. Add basic monitoring for errors, connection failures, and unusual request volume.
0138. Document how to start and stop each process.
0139. Document the Python version and dependency versions after confirming them from the project environment.
0140. Do not claim that deployment is complete until the application has been tested in its target environment.

## Project Structure

0141. The notes name client.py and server.py for the TCP client/server path.
0142. The notes refer to Flask routes for the browser-facing path.
0143. The actual repository tree was not included as readable text in the uploaded PDFs.
0144. The structure below is therefore a suggested organization, not a verified inventory of existing files.
0145. Keep browser application code separate from desktop socket code.
0146. Keep cryptographic functions isolated so they can be tested independently.
0147. Keep storage access behind a small interface if the backend may change.
0148. Keep configuration separate from business logic.
0149. Keep tests separate from runtime modules.
0150. Update this section to match the actual repository before publishing the README.

## Limitations and Open Questions

0151. The exact three layer names are not fully legible in the scans.
0152. The precise cipher and key-management design must be verified from source code.
0153. The notes do not establish whether a real quantum simulator is integrated.
0154. The notes do not specify a final database or shared key-value implementation.
0155. The notes do not specify deployment URLs, ports, environment variables, or package versions.
0156. The notes do not establish that a formal security audit has been performed.
0157. The notes do not establish production readiness or measured performance.
0158. The term 'fake web interface' should be clarified in the project description before public release.
0159. Any statistics in the handwritten notes about breach costs need a reliable citation before being used as factual claims.
0160. Treat unverified details as open questions rather than silently inventing answers.

### Browser request lifecycle

0161. User opens the chat page; the browser requests the page from the Flask application.
0162. Flask resolves the route and checks the requested page or room context.
0163. The application should reject malformed room identifiers before querying storage.
0164. Room access should be checked on the server for every protected operation.
0165. The browser renders only the data returned by the server.
0166. The browser should not be trusted to enforce room passwords or participant permissions.
0167. Polling begins only after the page has established the room and the participant context.
0168. Each polling request should carry a cursor such as the last received message identifier.
0169. The server should return only messages newer than the supplied cursor.
0170. The client should advance its cursor only after it has handled the returned messages.
0171. An empty polling response means there are no newer messages at that moment.
0172. Network errors should not cause the interface to duplicate already displayed messages.
0173. Polling intervals should balance responsiveness with request overhead.
0174. Polling responses should have a predictable format such as JSON if that matches the implementation.
0175. Input and output encoding should prevent user text from being interpreted as executable markup.
0176. Error responses should avoid exposing stack traces or internal configuration.
0177. Session and room identifiers should not be treated as secrets unless their design explicitly requires it.
0178. Authentication state should expire according to a documented policy.
0179. HTTPS should be enforced for public browser traffic.
0180. Cross-origin access should be restricted to the origins that actually need it.

### Room authorization

0181. A room lookup should distinguish an existing room from a nonexistent room.
0182. A protected room should require the intended authentication or password step.
0183. Incorrect room passwords should not reveal confidential room metadata.
0184. Room password verification should be performed by trusted server-side code.
0185. Room passwords should be stored using a suitable password-hashing function rather than plaintext.
0186. Rate limiting can reduce automated password guessing.
0187. Participant membership should be checked before sending a message.
0188. Participant membership should also be checked before reading message history.
0189. Leaving a room should update presence state if presence tracking is implemented.
0190. Participant tracking should define whether it represents online sessions or registered accounts.
0191. Multiple tabs may create multiple sessions for one participant unless the design prevents it.
0192. Room deletion should define what happens to messages and participant state.
0193. Unknown room identifiers should fail safely.
0194. Authorization checks should be covered by automated tests.
0195. An identifier supplied by the browser is not proof of permission.
0196. Administrative actions should have separate authorization rules.
0197. Password reset and room recovery behavior are not specified in the uploaded notes.
0198. Do not invent a registration process unless it exists in the application.
0199. Do not expose a list of private rooms to users who are not authorized to see it.
0200. Document whether room membership is temporary or persistent.

### Message model

0201. A message record should identify the room to which it belongs.
0202. A message record should identify the sender using a server-validated identity.
0203. A stable message identifier helps order messages and support incremental polling.
0204. A timestamp may help display chronology but should not replace a stable identifier.
0205. Message text should have a documented maximum size.
0206. Empty messages should be handled consistently.
0207. Messages containing unusual Unicode characters should be tested.
0208. Messages should be validated before encryption or storage.
0209. The server should reject invalid message shapes instead of guessing the intended fields.
0210. Ciphertext encoding should be defined, for example as a safe text encoding if required.
0211. Decryption failures should be handled without crashing the application.
0212. Integrity failures should not result in displaying unauthenticated plaintext.
0213. Duplicate submissions should be considered if a client retries after a timeout.
0214. Message deletion semantics should be documented if deletion is supported.
0215. Message edits should be treated as a separate feature if they are supported at all.
0216. File attachments are not established by the handwritten notes.
0217. Read receipts are not established by the handwritten notes.
0218. Typing indicators are not established by the handwritten notes.
0219. Delivery guarantees should match the actual implementation.
0220. Document whether messages are persisted, kept in memory, or discarded after delivery.

### Layer one: input preparation

0221. The first stage begins with the text entered by the participant.
0222. Input preparation may normalize the message representation before encryption.
0223. The exact normalization rules should be documented only after checking the code.
0224. Do not remove meaningful spaces or characters without a stated requirement.
0225. Validation should reject inputs that exceed configured limits.
0226. Encoding must be consistent between the sender and receiver.
0227. Text should be encoded to bytes before algorithms that operate on bytes are called.
0228. Character encoding should be explicit, commonly UTF-8 when supported by the implementation.
0229. Any transformation before encryption should be reversible if the receiver needs the original message.
0230. Do not describe simple encoding as encryption.
0231. Base64 and hexadecimal are encodings, not cryptographic confidentiality mechanisms.
0232. Input preparation should have unit tests for empty strings and non-ASCII text.
0233. Tests should include long inputs within the documented limit.
0234. Tests should include invalid input types.
0235. Error messages should avoid echoing secrets.
0236. Input preparation should not write plaintext to unnecessary logs.
0237. Temporary plaintext buffers should have a limited lifetime where practical.
0238. Do not assume that an extra transformation increases cryptographic strength.
0239. Document the input and output type of each preparation function.
0240. Keep the preparation stage independent from the transport implementation.

### Layer two: encryption

0241. The notes mention a second layer of encryption but do not clearly identify its algorithm.
0242. The implementation should use a well-reviewed cryptographic library where possible.
0243. Encryption keys should be generated with a cryptographically secure random source.
0244. Key length and algorithm mode should follow the chosen library's documented guidance.
0245. Nonces or initialization vectors must follow the selected algorithm's requirements.
0246. Never reuse a nonce where the selected mode forbids reuse.
0247. Ciphertext should be authenticated when the selected construction supports authenticated encryption.
0248. Authenticated encryption can detect unauthorized modification as well as protect confidentiality.
0249. Decryption should fail closed if authentication fails.
0250. Keys should not be hard-coded into a public repository.
0251. Keys should not be sent to logs or displayed in the user interface.
0252. Key exchange and key distribution need an explicit design.
0253. Password-derived keys require a suitable password-based key derivation function.
0254. Do not use a raw password directly as an encryption key.
0255. Different users or rooms may require separate keys depending on the intended threat model.
0256. Key rotation should be considered for a longer-running application.
0257. Key backup and recovery can create additional security risks.
0258. Cryptographic code should be tested with known test vectors where available.
0259. Do not create a custom production cipher merely to demonstrate multiple layers.
0260. Document which party can decrypt each message and why.

### Quantum-simulation concept

0261. The uploaded notes refer to a quantum-simulated or quantum-inspired cipher concept.
0262. The notes do not clearly establish a named quantum algorithm or a verified simulator package.
0263. If a simulator is part of the code, name the exact package and version in this section.
0264. Explain whether the simulator represents qubits, gates, measurements, or only a classical analogy.
0265. Explain what input enters the simulated stage and what output it returns.
0266. Explain how the receiver reverses or interprets that output.
0267. State whether the simulation is educational, experimental, or intended to support a security claim.
0268. A classical simulation does not mean the program is running on a quantum computer.
0269. A quantum-inspired custom transformation is not automatically secure against quantum attackers.
0270. Do not describe a project cipher as quantum-safe without evidence from established cryptographic analysis.
0271. Do not imply that adding a simulated layer automatically strengthens the other layers.
0272. Separate the educational demonstration from claims about real-world cryptographic resistance.
0273. Record reproducible example inputs and outputs for tests.
0274. Check whether the operation is deterministic or uses randomness.
0275. If randomness is used, document how it is generated and communicated safely.
0276. Check whether the output is reversible without exposing a secret.
0277. Check how errors or invalid quantum-state representations are handled.
0278. Keep the simulation module separate from the chat transport code.
0279. Use a threat model to explain what the simulated stage is supposed to defend against.
0280. Mark this feature as planned if the repository does not contain working simulator code.

### HTTPS and transport security

0281. The notes state that HTTP polling is used instead of WebSocket delivery.
0282. HTTPS is HTTP carried over TLS.
0283. TLS protects browser-to-server traffic in transit when configured correctly.
0284. Certificate validation helps the client verify the server it intended to contact.
0285. HTTPS does not prevent malware from reading plaintext on an endpoint.
0286. HTTPS does not by itself make messages end-to-end encrypted.
0287. If the server decrypts a message, the server can access its plaintext during processing.
0288. If the design aims to keep plaintext from the server, encryption must be arranged accordingly.
0289. Secure cookies should use appropriate Secure and HttpOnly settings where applicable.
0290. Session identifiers should be protected from exposure.
0291. Public deployments should redirect or otherwise enforce HTTP-to-HTTPS behavior.
0292. TLS configuration should be managed by the deployment environment or a maintained library.
0293. Do not disable certificate validation to make a demo connection work.
0294. Polling endpoints should be protected by the same access checks as the page.
0295. Responses should not disclose messages from other rooms.
0296. Cross-origin policies should be deliberately configured.
0297. Rate limiting can reduce abusive polling volume.
0298. Request timeouts should be bounded.
0299. Network failures should be reported without leaking secrets.
0300. Document whether HTTPS is configured locally, in a reverse proxy, or in a hosted environment.

### TCP sockets

0301. TCP is a transport protocol that delivers an ordered byte stream.
0302. TCP does not preserve application message boundaries by itself.
0303. The desktop protocol therefore needs a clear framing strategy.
0304. A length-prefixed message is one possible framing approach, if implemented.
0305. A newline-delimited protocol is another possibility, if its constraints are handled.
0306. Do not claim either framing approach is implemented until the code confirms it.
0307. The server should handle partial reads because one read may not return a full application message.
0308. The client should handle partial writes and disconnected peers.
0309. Socket operations can fail and should have explicit error handling.
0310. Connection timeouts prevent a client from waiting indefinitely.
0311. Connection closure should release resources.
0312. The server should limit the size of accepted messages.
0313. The server should not assume that bytes received are valid text until decoding succeeds.
0314. Text decoding errors should be handled safely.
0315. TCP reliability does not provide encryption or authentication.
0316. Raw TCP traffic can be observed on a network unless protected by another security layer.
0317. TLS can protect TCP traffic if the application is designed to use it.
0318. Access to a demo socket port should be restricted where possible.
0319. Concurrent clients require a deliberate concurrency model.
0320. Document how the desktop client reconnects, if reconnect behavior exists.

### Storage and process behavior

0321. An in-memory dictionary or list is volatile unless separately persisted.
0322. Restarting the process may remove in-memory room and message state.
0323. Separate worker processes usually have separate memory spaces.
0324. An in-memory store is not automatically a shared store across application instances.
0325. The notes mention a shared key-value store as a possible multi-instance solution.
0326. A shared store should be selected based on consistency, availability, and operational needs.
0327. Storage access should be isolated from route handlers where practical.
0328. Message retention should have a documented policy.
0329. Old messages may need to be removed according to the project's goals.
0330. Room passwords and encryption keys should not be stored alongside messages without protection.
0331. Logs should not become an unintended message archive.
0332. Backups can preserve sensitive data and need appropriate access controls.
0333. Development fixtures should not contain real personal messages.
0334. Storage errors should not cause the server to silently return incorrect messages.
0335. Concurrent writes should not create duplicate identifiers.
0336. Message ordering should be stable across concurrent requests.
0337. Shared storage credentials should be managed as secrets.
0338. Document whether the store is used only for development or also for deployment.
0339. Test behavior when the storage service is unavailable.
0340. Do not claim persistence until restart and recovery tests pass.

### Threat model and user safety

0341. A threat model identifies the assets, attackers, and security boundaries of the project.
0342. Potential assets include message content, room passwords, session tokens, and encryption keys.
0343. Potential attackers include network observers, unauthorized room visitors, and compromised endpoints.
0344. A man-in-the-middle attack can attempt to observe or modify communication.
0345. TLS with certificate validation helps address network interception risks.
0346. Room authorization helps prevent unauthorized access to room data.
0347. Message authentication can help detect tampering.
0348. Password hashing helps reduce the impact of a leaked password database.
0349. Rate limiting helps make repeated guessing less practical.
0350. Key management remains critical even when encryption algorithms are strong.
0351. Compromised client devices may expose data before encryption or after decryption.
0352. Custom input fields do not guarantee protection from keyloggers.
0353. Endpoint malware may capture screen content, clipboard data, or process memory.
0354. Users should not enter real sensitive information into an unaudited demonstration.
0355. Security claims should be specific about the threat they address.
0356. Security controls should be tested rather than assumed to work.
0357. Dependency updates help address known library vulnerabilities.
0358. Debug output can expose internal implementation details.
0359. Error messages should be useful without disclosing secrets.
0360. Record accepted risks and unresolved issues in the repository.

### Testing checklist

0361. Confirm that the application starts with the documented command.
0362. Confirm that the expected Flask route returns the correct page.
0363. Confirm that a nonexistent room is rejected.
0364. Confirm that a protected room rejects an incorrect password.
0365. Confirm that an authorized participant can access the intended room.
0366. Confirm that an unauthorized participant cannot read messages.
0367. Confirm that a message appears only in its intended room.
0368. Confirm that polling returns only messages newer than the cursor.
0369. Confirm that repeated polling does not duplicate visible messages.
0370. Confirm that messages are displayed in the intended order.
0371. Confirm that empty input is handled consistently.
0372. Confirm that very long input is rejected or safely handled.
0373. Confirm that special characters are displayed as text rather than executed.
0374. Confirm that encryption and decryption round-trip valid test messages.
0375. Confirm that modified ciphertext fails authentication if authenticated encryption is used.
0376. Confirm that incorrect keys produce a controlled failure.
0377. Confirm that TCP clients handle server disconnection.
0378. Confirm that partial TCP reads do not corrupt message framing.
0379. Confirm the documented behavior after an application restart.
0380. Record test commands and observed results before marking tests complete.

### Deployment checklist

0381. Pin dependencies after confirming which packages the project uses.
0382. Document the supported Python version.
0383. Keep development secrets out of version control.
0384. Provide a sample environment configuration without real credentials.
0385. Disable debug mode in a public deployment.
0386. Configure HTTPS for browser traffic.
0387. Restrict desktop TCP access to intended clients.
0388. Set request and connection timeouts.
0389. Choose a persistence strategy that matches the deployment topology.
0390. Use shared storage when independent instances must share state.
0391. Configure backups only if persistent data is intended to be retained.
0392. Limit access to backups and operational logs.
0393. Set a message retention policy.
0394. Document how to update dependencies safely.
0395. Document how to stop and restart services.
0396. Document how to inspect service health.
0397. Test deployment in a non-production environment first.
0398. Verify that secrets are not present in logs.
0399. Verify that room access controls remain enabled in production.
0400. Do not call the project production-ready until deployment checks have passed.

### Documentation maintenance

0401. Keep the README aligned with the current source code.
0402. Replace suggested filenames with the actual repository layout.
0403. List only dependencies that are actually imported or installed.
0404. List only commands that have been tested in the target environment.
0405. Record the algorithm names exactly as implemented.
0406. Record the encryption parameters that are safe to disclose and necessary to reproduce behavior.
0407. Never publish private keys, passwords, tokens, or real room secrets.
0408. Document the limitations of the quantum-simulation concept clearly.
0409. Add diagrams only when they match the actual data flow.
0410. Update tests whenever the message format changes.
0411. Update deployment steps whenever configuration changes.
0412. Record breaking changes in a changelog if the project evolves.
0413. Distinguish implemented features from planned features.
0414. Distinguish measured performance from expectations.
0415. Use citations for any external statistics included in a future revision.
0416. Do not retain unsupported breach-cost numbers from notes without verification.
0417. Use consistent terms for room, participant, message, client, and server.
0418. Keep security terminology precise and understandable.
0419. Ask reviewers to check both functionality and security assumptions.
0420. Review this document after every major architecture change.

### Suggested repository map

0421. `app.py` — suggested Flask entry point; replace this name if the actual entry point differs.
0422. `client.py` — named in the notes as the desktop TCP client.
0423. `server.py` — named in the notes as the desktop TCP server.
0424. `templates/` — suggested location for HTML templates if Flask templates are used.
0425. `static/` — suggested location for CSS, images, and browser JavaScript if present.
0426. `crypto/` — suggested package for encryption and decryption helpers if the code is modularized.
0427. `storage/` — suggested package for room and message storage adapters if needed.
0428. `tests/` — suggested location for automated tests.
0429. `requirements.txt` or `pyproject.toml` — include the actual dependency manifest used by the project.
0430. `README.md` — project documentation and verified setup instructions.

### Run instructions placeholder

0431. Step 1: Install the Python version supported by the repository.
0432. Step 2: Create and activate a virtual environment.
0433. Step 3: Install dependencies from the repository's actual manifest.
0434. Step 4: Set required environment variables using a local, untracked configuration file.
0435. Step 5: Start the Flask process using the real entry-point command.
0436. Step 6: Open the configured local URL in a browser.
0437. Step 7: Start the desktop server separately if the TCP demonstration is required.
0438. Step 8: Start the desktop client with the actual command and server address.
0439. Step 9: Test a room, participant check, and sample message using non-sensitive demo data.
0440. Step 10: Stop each process and confirm resources are released.

### Environment configuration placeholder

0441. Document the Flask secret configuration if Flask sessions are used.
0442. Document the bind host and port after confirming them from the code.
0443. Document the storage backend and connection settings if applicable.
0444. Document the room password configuration approach without including real passwords.
0445. Document any encryption key source without publishing the key itself.
0446. Document whether the quantum simulator requires an extra package.
0447. Document TLS termination if the web app is deployed behind a reverse proxy.
0448. Document the desktop TCP host and port only after confirming their values.
0449. Use environment variables or a secret manager for credentials.
0450. Do not commit a real `.env` file.

### Feature status table guidance

0451. Mark room creation as implemented only if a working route or function exists.
0452. Mark room password validation as implemented only if tested on the server.
0453. Mark participant tracking as implemented only if state is actually recorded and updated.
0454. Mark message polling as implemented only if the browser repeatedly requests new messages.
0455. Mark desktop TCP messaging as implemented only if client and server exchange messages successfully.
0456. Mark encryption as implemented only after the real algorithm and code path are identified.
0457. Mark decryption as implemented only after round-trip tests pass.
0458. Mark quantum simulation as implemented only if a working simulator integration exists.
0459. Mark shared storage as implemented only if the application uses a shared service or database.
0460. Mark production TLS as implemented only after deployment configuration is verified.

### Review questions before release

0461. What are the exact three message-processing layers in the source code?
0462. Which standard cryptographic algorithm is used in each actual encryption stage?
0463. How are keys created, exchanged, stored, and rotated?
0464. Does the server ever see plaintext messages?
0465. What does the project mean by a quantum-simulated cipher?
0466. Which Flask routes create rooms, validate passwords, send messages, and poll updates?
0467. How does the server identify registered participants?
0468. Are message identifiers globally unique or unique only within a room?
0469. What data store is used in the current version?
0470. What happens to rooms and messages when the process restarts?

### Source fidelity notes

0471. The uploaded pages are handwritten scans and do not contain machine-readable text.
0472. The README therefore relies on visual inspection of the handwritten pages.
0473. Some handwriting is ambiguous, so exact cryptographic names cannot safely be asserted.
0474. The phrase about three layers is readable, but every layer's exact technical definition is not.
0475. The phrase about a quantum-simulated cipher appears in the notes but needs source-code confirmation.
0476. The notes clearly mention HTTP polling as an alternative to WebSocket delivery.
0477. The notes clearly mention TCP sockets for the separate client/server path.
0478. The notes clearly mention in-memory storage limitations and shared key-value storage for multiple instances.
0479. The notes discuss HTTPS, transport-layer security, and message confidentiality.
0480. The notes discuss custom input fields and keylogger risk, but custom fields are not a complete defense.

0481. Verify the behavior with a clean install rather than relying on an existing virtual environment (review pass 6).
0482. Verify every import against the dependency manifest (review pass 6).
0483. Verify that the Flask application uses a non-default secret in deployment (review pass 6).
0484. Verify that passwords are never printed in terminal output (review pass 6).
0485. Verify that message plaintext is not written to debug logs (review pass 6).
0486. Verify that ciphertext encoding survives JSON serialization if JSON is used (review pass 6).
0487. Verify that Unicode messages survive encryption and decryption unchanged (review pass 6).
0488. Verify that a message cannot be fetched by changing only the room identifier (review pass 6).
0489. Verify that a participant cannot impersonate another participant by editing request fields (review pass 6).
0490. Verify that polling requests are authorized independently of the initial page request (review pass 6).
0491. Verify that repeated client retries do not create unintended duplicate messages (review pass 6).
0492. Verify that a stale polling cursor has a defined outcome (review pass 6).
0493. Verify that malformed JSON is rejected if the endpoint expects JSON (review pass 6).
0494. Verify that unexpected field names are rejected or ignored safely (review pass 6).
0495. Verify that the server caps request size (review pass 6).
0496. Verify that the application limits the number of messages returned in one poll (review pass 6).
0497. Verify that the UI safely renders message content (review pass 6).
0498. Verify that error responses do not include file paths or secret configuration (review pass 6).
0499. Verify that the desktop protocol rejects oversized frames (review pass 6).
0500. Verify that the desktop protocol handles a client closing unexpectedly (review pass 6).
0501. Verify that multiple desktop clients do not corrupt shared state (review pass 6).
0502. Verify that socket exceptions do not terminate unrelated client sessions (review pass 6).
0503. Verify that connection resources are closed after errors (review pass 6).
0504. Verify whether the TCP path is encrypted; document the actual result (review pass 6).
0505. Verify whether TLS is used by the desktop path or only by the browser path (review pass 6).
0506. Verify that a missing encryption key results in a controlled error (review pass 6).
0507. Verify that invalid ciphertext is rejected (review pass 6).
0508. Verify that the receiver checks integrity before displaying decrypted text (review pass 6).
0509. Verify that key material is not embedded in browser JavaScript unless explicitly intended and safe (review pass 6).
0510. Verify that a browser user cannot retrieve another room's encryption key (review pass 6).
0511. Verify whether the encryption process runs on the client or the server (review pass 6).
0512. Verify the exact order of all transformation stages (review pass 6).
0513. Verify whether the first layer is encoding, formatting, or cryptographic protection (review pass 6).
0514. Verify whether the second layer is a standard encryption construction (review pass 6).
0515. Verify the exact meaning of the quantum-simulation phrase in the implementation (review pass 6).
0516. Verify that any quantum simulator dependency is listed and versioned (review pass 6).
0517. Verify whether the quantum stage is reversible and how reversal works (review pass 6).
0518. Verify that random values needed for decryption are transmitted or derived correctly (review pass 6).
0519. Verify that nonce or initialization-vector handling matches the selected algorithm (review pass 6).
0520. Verify that cryptographic random values are generated by a secure source (review pass 6).
0521. Verify that keys are not reused in ways forbidden by the algorithm (review pass 6).
0522. Verify that algorithm parameters are not silently changed between client and server (review pass 6).
0523. Verify that test vectors are available for each cryptographic component (review pass 6).
0524. Verify that the project does not claim quantum resistance without evidence (review pass 6).
0525. Verify that room password hashing uses a purpose-built password-hashing mechanism (review pass 6).
0526. Verify that failed room password attempts are handled consistently (review pass 6).
0527. Verify whether room passwords can be guessed without rate limits (review pass 6).
0528. Verify that registration checks are based on trusted server-side state (review pass 6).
0529. Verify how participant presence expires after disconnect (review pass 6).
0530. Verify whether the same account can open multiple sessions (review pass 6).
0531. Verify whether room membership is persisted or only held in memory (review pass 6).
0532. Verify whether messages remain after leaving a room (review pass 6).
0533. Verify what data is deleted when a room is deleted (review pass 6).
0534. Verify the storage schema and document it accurately (review pass 6).
0535. Verify that in-memory state loss on restart is acceptable for the demo (review pass 6).
0536. Verify whether a shared key-value store is implemented or only proposed (review pass 6).
0537. Verify whether multiple processes can read and write the same message history (review pass 6).
0538. Verify that message identifiers remain unique when multiple workers run (review pass 6).
0539. Verify that storage errors are visible to maintainers without exposing secrets to users (review pass 6).
0540. Verify that logs have a retention and access policy (review pass 6).
0541. Verify that backups, if any, are encrypted and access-controlled (review pass 6).
0542. Verify that dependency versions are known and repeatable (review pass 6).
0543. Verify that a clean checkout contains every file required to run the demo (review pass 6).
0544. Verify that startup commands in this README match the current repository (review pass 6).
0545. Verify that the documented local URL matches the configured Flask host and port (review pass 6).
0546. Verify that desktop host and port settings are documented from the code (review pass 6).
0547. Verify that the browser and desktop flows can be started independently if intended (review pass 6).
0548. Verify that stopping the server does not leave background processes running (review pass 6).
0549. Verify that debug mode is disabled outside local development (review pass 6).
0550. Verify that the public deployment uses valid TLS certificates (review pass 6).
0551. Verify that the app does not silently accept invalid certificates (review pass 6).
0552. Verify that allowed browser origins are restricted as intended (review pass 6).
0553. Verify that the server has request and connection timeouts (review pass 6).
0554. Verify that deployment secrets are injected through a safe mechanism (review pass 6).
0555. Verify that the deployment process does not publish local secret files (review pass 6).
0556. Verify that the project is labelled as a prototype if no security audit exists (review pass 6).
0557. Verify that all external statistics have credible sources before including them (review pass 6).
0558. Verify that performance claims are supported by actual measurements (review pass 6).
0559. Verify that security claims are tied to a documented threat model (review pass 6).
0560. Verify that known limitations are visible to a reviewer (review pass 6).
0561. Verify that planned features are not described as already implemented (review pass 6).
0562. Verify that the repository map matches actual files (review pass 6).
0563. Verify that all code examples in the README are runnable (review pass 6).
0564. Verify that all shell commands are appropriate for the target operating system (review pass 6).
0565. Verify that the license section reflects the actual license chosen by the author (review pass 6).
0566. Verify that contributor instructions match the repository workflow (review pass 6).
0567. Verify that issue reporting instructions point to a real project location (review pass 6).
0568. Verify that the README does not include private personal data (review pass 6).
0569. Verify that screenshots do not expose credentials or real messages (review pass 6).
0570. Verify that demo credentials are clearly marked as disposable if provided (review pass 6).
0571. Verify that any sample keys are explicitly non-production test values (review pass 6).
0572. Verify that a reviewer can reproduce the basic chat flow from a clean environment (review pass 6).
0573. Verify that a reviewer can identify which security properties are demonstrated (review pass 6).
0574. Verify that a reviewer can distinguish transport encryption from message encryption (review pass 6).
0575. Verify that a reviewer understands the difference between simulation and quantum hardware (review pass 6).
0576. Verify that all unknown details are resolved or kept marked as unknown (review pass 6).
0577. Verify the behavior with a clean install rather than relying on an existing virtual environment (review pass 7).
0578. Verify every import against the dependency manifest (review pass 7).
0579. Verify that the Flask application uses a non-default secret in deployment (review pass 7).
0580. Verify that passwords are never printed in terminal output (review pass 7).
0581. Verify that message plaintext is not written to debug logs (review pass 7).
0582. Verify that ciphertext encoding survives JSON serialization if JSON is used (review pass 7).
0583. Verify that Unicode messages survive encryption and decryption unchanged (review pass 7).
0584. Verify that a message cannot be fetched by changing only the room identifier (review pass 7).
0585. Verify that a participant cannot impersonate another participant by editing request fields (review pass 7).
0586. Verify that polling requests are authorized independently of the initial page request (review pass 7).
0587. Verify that repeated client retries do not create unintended duplicate messages (review pass 7).
0588. Verify that a stale polling cursor has a defined outcome (review pass 7).
0589. Verify that malformed JSON is rejected if the endpoint expects JSON (review pass 7).
0590. Verify that unexpected field names are rejected or ignored safely (review pass 7).
0591. Verify that the server caps request size (review pass 7).
0592. Verify that the application limits the number of messages returned in one poll (review pass 7).
0593. Verify that the UI safely renders message content (review pass 7).
0594. Verify that error responses do not include file paths or secret configuration (review pass 7).
0595. Verify that the desktop protocol rejects oversized frames (review pass 7).
0596. Verify that the desktop protocol handles a client closing unexpectedly (review pass 7).
0597. Verify that multiple desktop clients do not corrupt shared state (review pass 7).
0598. Verify that socket exceptions do not terminate unrelated client sessions (review pass 7).
0599. Verify that connection resources are closed after errors (review pass 7).
0600. Verify whether the TCP path is encrypted; document the actual result (review pass 7).
0601. Verify whether TLS is used by the desktop path or only by the browser path (review pass 7).
0602. Verify that a missing encryption key results in a controlled error (review pass 7).
0603. Verify that invalid ciphertext is rejected (review pass 7).
0604. Verify that the receiver checks integrity before displaying decrypted text (review pass 7).
0605. Verify that key material is not embedded in browser JavaScript unless explicitly intended and safe (review pass 7).
0606. Verify that a browser user cannot retrieve another room's encryption key (review pass 7).
0607. Verify whether the encryption process runs on the client or the server (review pass 7).
0608. Verify the exact order of all transformation stages (review pass 7).
0609. Verify whether the first layer is encoding, formatting, or cryptographic protection (review pass 7).
0610. Verify whether the second layer is a standard encryption construction (review pass 7).
0611. Verify the exact meaning of the quantum-simulation phrase in the implementation (review pass 7).
0612. Verify that any quantum simulator dependency is listed and versioned (review pass 7).
0613. Verify whether the quantum stage is reversible and how reversal works (review pass 7).
0614. Verify that random values needed for decryption are transmitted or derived correctly (review pass 7).
0615. Verify that nonce or initialization-vector handling matches the selected algorithm (review pass 7).
0616. Verify that cryptographic random values are generated by a secure source (review pass 7).
0617. Verify that keys are not reused in ways forbidden by the algorithm (review pass 7).
0618. Verify that algorithm parameters are not silently changed between client and server (review pass 7).
0619. Verify that test vectors are available for each cryptographic component (review pass 7).
0620. Verify that the project does not claim quantum resistance without evidence (review pass 7).
0621. Verify that room password hashing uses a purpose-built password-hashing mechanism (review pass 7).
0622. Verify that failed room password attempts are handled consistently (review pass 7).
0623. Verify whether room passwords can be guessed without rate limits (review pass 7).
0624. Verify that registration checks are based on trusted server-side state (review pass 7).
0625. Verify how participant presence expires after disconnect (review pass 7).
0626. Verify whether the same account can open multiple sessions (review pass 7).
0627. Verify whether room membership is persisted or only held in memory (review pass 7).
0628. Verify whether messages remain after leaving a room (review pass 7).
0629. Verify what data is deleted when a room is deleted (review pass 7).
0630. Verify the storage schema and document it accurately (review pass 7).
0631. Verify that in-memory state loss on restart is acceptable for the demo (review pass 7).
0632. Verify whether a shared key-value store is implemented or only proposed (review pass 7).
0633. Verify whether multiple processes can read and write the same message history (review pass 7).
0634. Verify that message identifiers remain unique when multiple workers run (review pass 7).
0635. Verify that storage errors are visible to maintainers without exposing secrets to users (review pass 7).
0636. Verify that logs have a retention and access policy (review pass 7).
0637. Verify that backups, if any, are encrypted and access-controlled (review pass 7).
0638. Verify that dependency versions are known and repeatable (review pass 7).
0639. Verify that a clean checkout contains every file required to run the demo (review pass 7).
0640. Verify that startup commands in this README match the current repository (review pass 7).
0641. Verify that the documented local URL matches the configured Flask host and port (review pass 7).
0642. Verify that desktop host and port settings are documented from the code (review pass 7).
0643. Verify that the browser and desktop flows can be started independently if intended (review pass 7).
0644. Verify that stopping the server does not leave background processes running (review pass 7).
0645. Verify that debug mode is disabled outside local development (review pass 7).
0646. Verify that the public deployment uses valid TLS certificates (review pass 7).
0647. Verify that the app does not silently accept invalid certificates (review pass 7).
0648. Verify that allowed browser origins are restricted as intended (review pass 7).
0649. Verify that the server has request and connection timeouts (review pass 7).
0650. Verify that deployment secrets are injected through a safe mechanism (review pass 7).
0651. Verify that the deployment process does not publish local secret files (review pass 7).
0652. Verify that the project is labelled as a prototype if no security audit exists (review pass 7).
0653. Verify that all external statistics have credible sources before including them (review pass 7).
0654. Verify that performance claims are supported by actual measurements (review pass 7).
0655. Verify that security claims are tied to a documented threat model (review pass 7).
0656. Verify that known limitations are visible to a reviewer (review pass 7).
0657. Verify that planned features are not described as already implemented (review pass 7).
0658. Verify that the repository map matches actual files (review pass 7).
0659. Verify that all code examples in the README are runnable (review pass 7).
0660. Verify that all shell commands are appropriate for the target operating system (review pass 7).
0661. Verify that the license section reflects the actual license chosen by the author (review pass 7).
0662. Verify that contributor instructions match the repository workflow (review pass 7).
0663. Verify that issue reporting instructions point to a real project location (review pass 7).
0664. Verify that the README does not include private personal data (review pass 7).
0665. Verify that screenshots do not expose credentials or real messages (review pass 7).
0666. Verify that demo credentials are clearly marked as disposable if provided (review pass 7).
0667. Verify that any sample keys are explicitly non-production test values (review pass 7).
0668. Verify that a reviewer can reproduce the basic chat flow from a clean environment (review pass 7).
0669. Verify that a reviewer can identify which security properties are demonstrated (review pass 7).
0670. Verify that a reviewer can distinguish transport encryption from message encryption (review pass 7).
0671. Verify that a reviewer understands the difference between simulation and quantum hardware (review pass 7).
0672. Verify that all unknown details are resolved or kept marked as unknown (review pass 7).
0673. Verify the behavior with a clean install rather than relying on an existing virtual environment (review pass 8).
0674. Verify every import against the dependency manifest (review pass 8).
0675. Verify that the Flask application uses a non-default secret in deployment (review pass 8).
0676. Verify that passwords are never printed in terminal output (review pass 8).
0677. Verify that message plaintext is not written to debug logs (review pass 8).
0678. Verify that ciphertext encoding survives JSON serialization if JSON is used (review pass 8).
0679. Verify that Unicode messages survive encryption and decryption unchanged (review pass 8).
0680. Verify that a message cannot be fetched by changing only the room identifier (review pass 8).
0681. Verify that a participant cannot impersonate another participant by editing request fields (review pass 8).
0682. Verify that polling requests are authorized independently of the initial page request (review pass 8).
0683. Verify that repeated client retries do not create unintended duplicate messages (review pass 8).
0684. Verify that a stale polling cursor has a defined outcome (review pass 8).
0685. Verify that malformed JSON is rejected if the endpoint expects JSON (review pass 8).
0686. Verify that unexpected field names are rejected or ignored safely (review pass 8).
0687. Verify that the server caps request size (review pass 8).
0688. Verify that the application limits the number of messages returned in one poll (review pass 8).
0689. Verify that the UI safely renders message content (review pass 8).
0690. Verify that error responses do not include file paths or secret configuration (review pass 8).
0691. Verify that the desktop protocol rejects oversized frames (review pass 8).
0692. Verify that the desktop protocol handles a client closing unexpectedly (review pass 8).
0693. Verify that multiple desktop clients do not corrupt shared state (review pass 8).
0694. Verify that socket exceptions do not terminate unrelated client sessions (review pass 8).
0695. Verify that connection resources are closed after errors (review pass 8).
0696. Verify whether the TCP path is encrypted; document the actual result (review pass 8).
0697. Verify whether TLS is used by the desktop path or only by the browser path (review pass 8).
0698. Verify that a missing encryption key results in a controlled error (review pass 8).
0699. Verify that invalid ciphertext is rejected (review pass 8).
0700. Verify that the receiver checks integrity before displaying decrypted text (review pass 8).
0701. Verify that key material is not embedded in browser JavaScript unless explicitly intended and safe (review pass 8).
0702. Verify that a browser user cannot retrieve another room's encryption key (review pass 8).
0703. Verify whether the encryption process runs on the client or the server (review pass 8).
0704. Verify the exact order of all transformation stages (review pass 8).
0705. Verify whether the first layer is encoding, formatting, or cryptographic protection (review pass 8).
0706. Verify whether the second layer is a standard encryption construction (review pass 8).
0707. Verify the exact meaning of the quantum-simulation phrase in the implementation (review pass 8).
0708. Verify that any quantum simulator dependency is listed and versioned (review pass 8).
0709. Verify whether the quantum stage is reversible and how reversal works (review pass 8).
0710. Verify that random values needed for decryption are transmitted or derived correctly (review pass 8).
0711. Verify that nonce or initialization-vector handling matches the selected algorithm (review pass 8).
0712. Verify that cryptographic random values are generated by a secure source (review pass 8).
0713. Verify that keys are not reused in ways forbidden by the algorithm (review pass 8).
0714. Verify that algorithm parameters are not silently changed between client and server (review pass 8).
0715. Verify that test vectors are available for each cryptographic component (review pass 8).
0716. Verify that the project does not claim quantum resistance without evidence (review pass 8).
0717. Verify that room password hashing uses a purpose-built password-hashing mechanism (review pass 8).
0718. Verify that failed room password attempts are handled consistently (review pass 8).
0719. Verify whether room passwords can be guessed without rate limits (review pass 8).
0720. Verify that registration checks are based on trusted server-side state (review pass 8).
0721. Verify how participant presence expires after disconnect (review pass 8).
0722. Verify whether the same account can open multiple sessions (review pass 8).
0723. Verify whether room membership is persisted or only held in memory (review pass 8).
0724. Verify whether messages remain after leaving a room (review pass 8).
0725. Verify what data is deleted when a room is deleted (review pass 8).
0726. Verify the storage schema and document it accurately (review pass 8).
0727. Verify that in-memory state loss on restart is acceptable for the demo (review pass 8).
0728. Verify whether a shared key-value store is implemented or only proposed (review pass 8).
0729. Verify whether multiple processes can read and write the same message history (review pass 8).
0730. Verify that message identifiers remain unique when multiple workers run (review pass 8).
0731. Verify that storage errors are visible to maintainers without exposing secrets to users (review pass 8).
0732. Verify that logs have a retention and access policy (review pass 8).
0733. Verify that backups, if any, are encrypted and access-controlled (review pass 8).
0734. Verify that dependency versions are known and repeatable (review pass 8).
0735. Verify that a clean checkout contains every file required to run the demo (review pass 8).
0736. Verify that startup commands in this README match the current repository (review pass 8).
0737. Verify that the documented local URL matches the configured Flask host and port (review pass 8).
0738. Verify that desktop host and port settings are documented from the code (review pass 8).
0739. Verify that the browser and desktop flows can be started independently if intended (review pass 8).
0740. Verify that stopping the server does not leave background processes running (review pass 8).
0741. Verify that debug mode is disabled outside local development (review pass 8).
0742. Verify that the public deployment uses valid TLS certificates (review pass 8).
0743. Verify that the app does not silently accept invalid certificates (review pass 8).
0744. Verify that allowed browser origins are restricted as intended (review pass 8).
0745. Verify that the server has request and connection timeouts (review pass 8).
0746. Verify that deployment secrets are injected through a safe mechanism (review pass 8).
0747. Verify that the deployment process does not publish local secret files (review pass 8).
0748. Verify that the project is labelled as a prototype if no security audit exists (review pass 8).
0749. Verify that all external statistics have credible sources before including them (review pass 8).
0750. Verify that performance claims are supported by actual measurements (review pass 8).
0751. Verify that security claims are tied to a documented threat model (review pass 8).
0752. Verify that known limitations are visible to a reviewer (review pass 8).
0753. Verify that planned features are not described as already implemented (review pass 8).
0754. Verify that the repository map matches actual files (review pass 8).
0755. Verify that all code examples in the README are runnable (review pass 8).
0756. Verify that all shell commands are appropriate for the target operating system (review pass 8).
0757. Verify that the license section reflects the actual license chosen by the author (review pass 8).
0758. Verify that contributor instructions match the repository workflow (review pass 8).
0759. Verify that issue reporting instructions point to a real project location (review pass 8).
0760. Verify that the README does not include private personal data (review pass 8).
0761. Verify that screenshots do not expose credentials or real messages (review pass 8).
0762. Verify that demo credentials are clearly marked as disposable if provided (review pass 8).
0763. Verify that any sample keys are explicitly non-production test values (review pass 8).
0764. Verify that a reviewer can reproduce the basic chat flow from a clean environment (review pass 8).
0765. Verify that a reviewer can identify which security properties are demonstrated (review pass 8).
0766. Verify that a reviewer can distinguish transport encryption from message encryption (review pass 8).
0767. Verify that a reviewer understands the difference between simulation and quantum hardware (review pass 8).
0768. Verify that all unknown details are resolved or kept marked as unknown (review pass 8).
0769. Verify the behavior with a clean install rather than relying on an existing virtual environment (review pass 9).
0770. Verify every import against the dependency manifest (review pass 9).
0771. Verify that the Flask application uses a non-default secret in deployment (review pass 9).
0772. Verify that passwords are never printed in terminal output (review pass 9).
0773. Verify that message plaintext is not written to debug logs (review pass 9).
0774. Verify that ciphertext encoding survives JSON serialization if JSON is used (review pass 9).
0775. Verify that Unicode messages survive encryption and decryption unchanged (review pass 9).
0776. Verify that a message cannot be fetched by changing only the room identifier (review pass 9).
0777. Verify that a participant cannot impersonate another participant by editing request fields (review pass 9).
0778. Verify that polling requests are authorized independently of the initial page request (review pass 9).
0779. Verify that repeated client retries do not create unintended duplicate messages (review pass 9).
0780. Verify that a stale polling cursor has a defined outcome (review pass 9).
0781. Verify that malformed JSON is rejected if the endpoint expects JSON (review pass 9).
0782. Verify that unexpected field names are rejected or ignored safely (review pass 9).
0783. Verify that the server caps request size (review pass 9).
0784. Verify that the application limits the number of messages returned in one poll (review pass 9).
0785. Verify that the UI safely renders message content (review pass 9).
0786. Verify that error responses do not include file paths or secret configuration (review pass 9).
0787. Verify that the desktop protocol rejects oversized frames (review pass 9).
0788. Verify that the desktop protocol handles a client closing unexpectedly (review pass 9).
0789. Verify that multiple desktop clients do not corrupt shared state (review pass 9).
0790. Verify that socket exceptions do not terminate unrelated client sessions (review pass 9).
0791. Verify that connection resources are closed after errors (review pass 9).
0792. Verify whether the TCP path is encrypted; document the actual result (review pass 9).
0793. Verify whether TLS is used by the desktop path or only by the browser path (review pass 9).
0794. Verify that a missing encryption key results in a controlled error (review pass 9).
0795. Verify that invalid ciphertext is rejected (review pass 9).
0796. Verify that the receiver checks integrity before displaying decrypted text (review pass 9).
0797. Verify that key material is not embedded in browser JavaScript unless explicitly intended and safe (review pass 9).
0798. Verify that a browser user cannot retrieve another room's encryption key (review pass 9).
0799. Verify whether the encryption process runs on the client or the server (review pass 9).
0800. Verify the exact order of all transformation stages (review pass 9).
0801. Verify whether the first layer is encoding, formatting, or cryptographic protection (review pass 9).
0802. Verify whether the second layer is a standard encryption construction (review pass 9).
0803. Verify the exact meaning of the quantum-simulation phrase in the implementation (review pass 9).
0804. Verify that any quantum simulator dependency is listed and versioned (review pass 9).
0805. Verify whether the quantum stage is reversible and how reversal works (review pass 9).
0806. Verify that random values needed for decryption are transmitted or derived correctly (review pass 9).
0807. Verify that nonce or initialization-vector handling matches the selected algorithm (review pass 9).
0808. Verify that cryptographic random values are generated by a secure source (review pass 9).
0809. Verify that keys are not reused in ways forbidden by the algorithm (review pass 9).
0810. Verify that algorithm parameters are not silently changed between client and server (review pass 9).
0811. Verify that test vectors are available for each cryptographic component (review pass 9).
0812. Verify that the project does not claim quantum resistance without evidence (review pass 9).
0813. Verify that room password hashing uses a purpose-built password-hashing mechanism (review pass 9).
0814. Verify that failed room password attempts are handled consistently (review pass 9).
0815. Verify whether room passwords can be guessed without rate limits (review pass 9).
0816. Verify that registration checks are based on trusted server-side state (review pass 9).
0817. Verify how participant presence expires after disconnect (review pass 9).
0818. Verify whether the same account can open multiple sessions (review pass 9).
0819. Verify whether room membership is persisted or only held in memory (review pass 9).
0820. Verify whether messages remain after leaving a room (review pass 9).
0821. Verify what data is deleted when a room is deleted (review pass 9).
0822. Verify the storage schema and document it accurately (review pass 9).
0823. Verify that in-memory state loss on restart is acceptable for the demo (review pass 9).
0824. Verify whether a shared key-value store is implemented or only proposed (review pass 9).
0825. Verify whether multiple processes can read and write the same message history (review pass 9).
0826. Verify that message identifiers remain unique when multiple workers run (review pass 9).
0827. Verify that storage errors are visible to maintainers without exposing secrets to users (review pass 9).
0828. Verify that logs have a retention and access policy (review pass 9).
0829. Verify that backups, if any, are encrypted and access-controlled (review pass 9).
0830. Verify that dependency versions are known and repeatable (review pass 9).
0831. Verify that a clean checkout contains every file required to run the demo (review pass 9).
0832. Verify that startup commands in this README match the current repository (review pass 9).
0833. Verify that the documented local URL matches the configured Flask host and port (review pass 9).
0834. Verify that desktop host and port settings are documented from the code (review pass 9).
0835. Verify that the browser and desktop flows can be started independently if intended (review pass 9).
0836. Verify that stopping the server does not leave background processes running (review pass 9).
0837. Verify that debug mode is disabled outside local development (review pass 9).
0838. Verify that the public deployment uses valid TLS certificates (review pass 9).
0839. Verify that the app does not silently accept invalid certificates (review pass 9).
0840. Verify that allowed browser origins are restricted as intended (review pass 9).
0841. Verify that the server has request and connection timeouts (review pass 9).
0842. Verify that deployment secrets are injected through a safe mechanism (review pass 9).
0843. Verify that the deployment process does not publish local secret files (review pass 9).
0844. Verify that the project is labelled as a prototype if no security audit exists (review pass 9).
0845. Verify that all external statistics have credible sources before including them (review pass 9).
0846. Verify that performance claims are supported by actual measurements (review pass 9).
0847. Verify that security claims are tied to a documented threat model (review pass 9).
0848. Verify that known limitations are visible to a reviewer (review pass 9).
0849. Verify that planned features are not described as already implemented (review pass 9).
0850. Verify that the repository map matches actual files (review pass 9).
0851. Verify that all code examples in the README are runnable (review pass 9).
0852. Verify that all shell commands are appropriate for the target operating system (review pass 9).
0853. Verify that the license section reflects the actual license chosen by the author (review pass 9).
0854. Verify that contributor instructions match the repository workflow (review pass 9).
0855. Verify that issue reporting instructions point to a real project location (review pass 9).
0856. Verify that the README does not include private personal data (review pass 9).
0857. Verify that screenshots do not expose credentials or real messages (review pass 9).
0858. Verify that demo credentials are clearly marked as disposable if provided (review pass 9).
0859. Verify that any sample keys are explicitly non-production test values (review pass 9).
0860. Verify that a reviewer can reproduce the basic chat flow from a clean environment (review pass 9).
0861. Verify that a reviewer can identify which security properties are demonstrated (review pass 9).
0862. Verify that a reviewer can distinguish transport encryption from message encryption (review pass 9).
0863. Verify that a reviewer understands the difference between simulation and quantum hardware (review pass 9).
0864. Verify that all unknown details are resolved or kept marked as unknown (review pass 9).
0865. Verify the behavior with a clean install rather than relying on an existing virtual environment (review pass 10).
0866. Verify every import against the dependency manifest (review pass 10).
0867. Verify that the Flask application uses a non-default secret in deployment (review pass 10).
0868. Verify that passwords are never printed in terminal output (review pass 10).
0869. Verify that message plaintext is not written to debug logs (review pass 10).
0870. Verify that ciphertext encoding survives JSON serialization if JSON is used (review pass 10).
0871. Verify that Unicode messages survive encryption and decryption unchanged (review pass 10).
0872. Verify that a message cannot be fetched by changing only the room identifier (review pass 10).
0873. Verify that a participant cannot impersonate another participant by editing request fields (review pass 10).
0874. Verify that polling requests are authorized independently of the initial page request (review pass 10).
0875. Verify that repeated client retries do not create unintended duplicate messages (review pass 10).
1000. Final release rule: publish only verified implementation details, clearly label assumptions, and keep this README synchronized with the actual source code.

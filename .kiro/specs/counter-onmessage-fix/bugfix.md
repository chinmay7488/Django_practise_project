# Bugfix Requirements Document

## Introduction

The live click counter relies on a WebSocket connection to keep every connected
browser in sync. When a click is registered, the server broadcasts the current
state (`current_count` and `users_online`) to all clients, and each client's
`socket.onmessage` handler is expected to update the count display and the
activity text.

In practice, the on-screen count and activity text never update when clicks
happen. Three defects combine to break the live-update flow:

1. The client `onmessage` handler calls `json.parse(...)` (lowercase), which is
   not a valid JavaScript API. This throws a `ReferenceError`, aborting the
   handler before it touches the DOM, so no server message is ever reflected in
   the UI.
2. The server's `connect()` calls `self.broadcast_room_state()` without
   `await`. Because it is an async coroutine, the initial state broadcast never
   executes, so a newly connected client receives no initial state message.
3. The server's `disconnect()` does not decrement `active_connections`, so the
   `users_online` count drifts upward over time and never reflects the true
   number of connected clients.

The user-facing symptom is the same for all three: messages sent (or that should
be sent) by the server are not correctly reflected in the browser UI.

## Bug Analysis

### Current Behavior (Defect)

1.1 WHEN the server sends a state message to the browser THEN the `socket.onmessage` handler calls `json.parse(event.data)`, throws a `ReferenceError` because `json` is undefined, and aborts before updating `count-display` or `activity`
1.2 WHEN a client connects to the WebSocket THEN `connect()` invokes `self.broadcast_room_state()` without `await`, so the coroutine never runs and the client receives no initial state message
1.3 WHEN a client disconnects from the WebSocket THEN `disconnect()` does not decrement `active_connections`, so `users_online` remains inflated and reports more users than are actually connected

### Expected Behavior (Correct)

2.1 WHEN the server sends a state message to the browser THEN the `socket.onmessage` handler SHALL parse the payload with `JSON.parse(event.data)` and update `count-display` with `current_count` and `activity` with `users_online`
2.2 WHEN a client connects to the WebSocket THEN `connect()` SHALL `await self.broadcast_room_state()` so the newly connected client receives the current state immediately
2.3 WHEN a client disconnects from the WebSocket THEN `disconnect()` SHALL decrement `active_connections` and broadcast the updated state so `users_online` reflects the true number of connected clients

### Unchanged Behavior (Regression Prevention)

3.1 WHEN a user taps the button and the socket is open THEN the system SHALL CONTINUE TO send the `{"action": "click_registered"}` payload via `JSON.stringify`
3.2 WHEN the server receives a `click_registered` action THEN the system SHALL CONTINUE TO increment `global_count` and broadcast the updated state to the group
3.3 WHEN the server packages a broadcast THEN the system SHALL CONTINUE TO send the payload keys `current_count` and `users_online` that the frontend reads
3.4 WHEN the socket connection closes THEN the system SHALL CONTINUE TO log the existing connection-severed message on the client

## Bug Condition

```pascal
FUNCTION isBugCondition(X)
  INPUT: X of type ClientServerInteraction
  OUTPUT: boolean

  // True for any interaction where the server has (or should have) state
  // that needs to be reflected in the browser UI.
  RETURN X.kind = "server_message_received"   // 1.1: onmessage cannot parse/apply state
      OR X.kind = "client_connect"            // 1.2: initial broadcast never awaited
      OR X.kind = "client_disconnect"         // 1.3: users_online not updated
END FUNCTION
```

```pascal
// Property: Fix Checking - server state is reflected in the UI
FOR ALL X WHERE isBugCondition(X) DO
  result ← F'(X)
  ASSERT ui_reflects_state(result)
         // count-display shows current_count,
         // activity shows the true users_online,
         // and no client-side ReferenceError is thrown
END FOR
```

```pascal
// Property: Preservation Checking - non-buggy paths are unchanged
FOR ALL X WHERE NOT isBugCondition(X) DO
  ASSERT F(X) = F'(X)
  // e.g. tap-to-send, click increment, broadcast payload keys, close logging
END FOR
```

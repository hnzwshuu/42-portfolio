*This project has been created as part of the 42 curriculum by shanazaw.*

## Description

Codexion simulates coders sharing USB dongles in a circular workspace. Each coder
needs both adjacent dongles to compile, then spends time debugging and refactoring.
Released dongles have a cooldown. Waiting requests are ordered by FIFO or Earliest
Deadline First (EDF), and a separate monitor stops the simulation on burnout.
Otherwise, it stops when every coder has completed the requested compile count.

## Instructions

Requirements: a C compiler, `make`, and POSIX threads. No additional library or
installation step is needed. Run commands from this directory:

```sh
make
./codexion 5 2000 200 200 200 10 0 fifo
./codexion 5 2000 200 200 200 7 0 edf
```

The Makefile uses `-Wall -Wextra -Werror -pthread`. `make clean` removes object
files, `make fclean` also removes the executable, and `make re` rebuilds it.
Generated header dependencies prevent unnecessary relinking and rebuild affected
objects when the public header changes.

All eight arguments are mandatory, in this exact order:

| Argument | Meaning |
| --- | --- |
| `number_of_coders` | Coders and dongles in the ring; at least 1. |
| `time_to_burnout` | Maximum milliseconds since the last compile start, or simulation start before the first compile. |
| `time_to_compile` | Milliseconds holding both dongles for one compile. |
| `time_to_debug` | Milliseconds debugging after a compile. |
| `time_to_refactor` | Milliseconds refactoring after debugging. |
| `number_of_compiles_required` | Completed compiles required for every coder. |
| `dongle_cooldown` | Milliseconds after release before a dongle is available again. |
| `scheduler` | Exactly `fifo` or `edf`, case sensitive. |

Numeric arguments contain decimal digits only and must be at most `INT_MAX`.
Signs, whitespace, empty strings, partial numbers, overflow, and incorrect
argument counts are rejected. Leading zeroes are accepted. All durations and the
required compile count may be zero. A required count of zero succeeds immediately
without allocating simulation resources, starting threads, or printing logs.
Burnout of zero otherwise means the initial deadline has already arrived.

Logs use `timestamp_in_ms coder_id message`; coder IDs start at 1. Burnout and
successful completion both exit with status 0. Invalid input or a runtime setup,
synchronization, clock, cleanup, or output failure exits with status 1.
Diagnostics identify the operation and its value or error code on standard error.

## Scheduling and timing choices

Every request receives a ticket while holding the coordinator mutex. FIFO compares
tickets. EDF orders `last_compile_start + time_to_burnout`, then ticket, then
coder ID. Because the burnout duration is shared by all coders, the comparator
can compare `last_start` directly without risking an overflowing deadline sum.
The final comparisons make equal deadlines deterministic. During the
running simulation, a queued coder's `last_start` stays unchanged until its
request leaves both heaps, so its priority does not change underneath the heap.

Each dongle has a binary min-heap with capacity two: only the two neighboring
coders can request it, and each coder has at most one outstanding request. A coder
is granted both dongles only when it is the root of both heaps, both are free, and
both cooldowns have expired. Requests remain queued while waiting; no coder takes
one dongle and waits for the other. For one coder, the sole dongle is taken once,
compiling is impossible, and the monitor eventually reports burnout.

All threads first wait behind a shared start barrier. Before releasing them, main
registers every initial pair request in even-index order followed by odd-index
order. This prevents a fast coder's second request from overtaking another
coder's first request before it was even registered. Once registration and thread
creation succeed, main samples the simulation epoch and sets every initial
`last_start` to it. All initial EDF keys move by the same amount, preserving their
heap ordering. Initial grant attempts depend on the ring's parity. For an even
coder count, all even-index coders attempt immediately and all odd-index coders
wait `compile + cooldown` microseconds. Each parity group uses disjoint dongle
pairs, allowing the entire group to compile concurrently. Serializing members of
that group would unnecessarily delay a feasible schedule.

For an odd coder count greater than one, the first and last even-index coders
share a dongle across the ring boundary, so parity groups are not independent.
Each successive initial rank instead waits
`ceil((compile + cooldown) / floor(number_of_coders / 2))` microseconds. This uses
the ring's maximum simultaneous pair count to spread initial resource demand.
The single-coder delay is zero. Debugging and refactoring are excluded from these
resource occupancy estimates. Later requests enter the queues immediately after
refactoring; the initial delay is not repeated between cycles.

Completed compiles are counted after the compile duration and release, rather
than when compiling starts. A coder that reaches its own required count continues
cycling and remains monitored until every coder has reached the count. No coder
silently retires early.

Durations and deadlines use monotonic microseconds internally. Cooldown begins at
the actual release time, not a predicted end or a rounded log timestamp. Logs
floor elapsed time to milliseconds. Default POSIX condition variables use a
realtime absolute timeout, so each wait converts the remaining monotonic duration
to a realtime deadline and requests at most 10 ms before rechecking its predicate.
This also lets stop checks proceed when a notification fails. Clock results and
deadline addition are checked before use. A wall-clock change during a wait can
still delay wakeup, including beyond the requested interval; stored simulation
deadlines remain monotonic.

## Blocking cases handled

- **Deadlock and Coffman's conditions:** mutual exclusion and non-preemption
  remain necessary for dongles. Atomic pair acquisition removes hold-and-wait for
  compilation resources. Actual dongle mutexes are always locked in ascending
  index order, removing circular mutex acquisition. The common total request
  order also prevents a cycle of conflicting queue priorities.
- **Arbitration and starvation:** both dongles honor their heap roots. A later
  FIFO request cannot bypass an earlier competing one, and EDF selects the
  earliest waiting deadline with deterministic ties. Initial staggering reduces
  contention and convoy formation in the reference cases. The subject does not
  mathematically define feasible parameters; strict per-dongle fairness with
  atomic pairs can still form convoys. 
- **Cooldown:** a release sets each owned dongle's `ready_at` under its mutex.
  Pair acquisition waits until the later of the two readiness times and rechecks
  ownership and priority after waking.
- **Burnout:** the monitor waits toward the nearest deadline in capped intervals
  and is notified when a compile changes it. Workers also check expiry and notify
  the monitor. The monitor emits the burnout message and stops the simulation
  under the same coordinator lock, making burnout the final state log. The
  delivery target is 10 ms; OS scheduling and blocked output prevent a hard
  realtime guarantee.
- **Startup and shutdown:** failed initialization destroys only initialized
  primitives. Failed thread creation stops and joins only created threads. Normal
  stop wakes both condition variables, joins all threads, then frees memory.
  Pending joins and failed destruction retain their storage and progress counters
  for a retry; storage is never forcibly freed while a thread may still use it.
- **Log serialization:** an output mutex protects whole lines and the three-line
  pair-acquisition/compile group. Writes use bounded interruption retries and
  handle partial writes; output is not deferred in a standard I/O buffer until
  process exit.
  State names are validated and line assembly is bounded.

## Thread synchronization mechanisms

There is one thread per coder plus one monitor. Main creates them, opens the start
barrier, joins them, and destroys shared resources. There are no global variables.

| Primitive | Protected state or purpose |
| --- | --- |
| `sim.lock` (`pthread_mutex_t`) | Start/stop state, tickets, compile timestamps, completion counts, and transitions involving queues and resources. |
| Each dongle's `mutex` | Its heap, owner, and cooldown readiness time. |
| `sim.log_lock` (`pthread_mutex_t`) | Serialized output. |
| `sim.event` (`pthread_cond_t`) | Start, resource/queue changes, phase waits, cooldown waits, and stop. |
| `sim.watch` (`pthread_cond_t`) | Monitor start, changed compile deadlines, expiry notifications, and stop. |

Every shared transition begins with `sim.lock`. Inside that transition, code may
take dongle mutexes in ascending index order, or the output mutex. It releases
dongle mutexes before logging and before any condition wait. A condition wait
holds neither dongle nor output mutex; POSIX atomically releases `sim.lock` while
sleeping and reacquires it before returning. All waits are inside loops that
recheck predicates, including after spurious wakeups.

For example, checking that both owners are zero and assigning both owners happen
in the same protected transition, preventing two coders from claiming the same
dongle. Updating `last_start` and signaling `watch` also happen under `sim.lock`,
so the monitor cannot read a partially updated transition. Stop broadcasts both
conditions, allowing waiting coders and the monitor to leave their loops. Coders
communicate through this shared resource state rather than sending messages to
one another.

The coordinator deliberately serializes bookkeeping. Compilation, debugging,
refactoring, and cooldown waits release it, allowing overlapping work. Heap
operations are constant-sized in this fixed ring; scans for the earliest deadline
are linear in the coder count, including worker liveness checks. This favors a
small, explainable implementation over scaling to arbitrarily many threads.

## Defensive API contracts

The command-line program supplies a zero-initialized simulation object and keeps
it alive until cleanup succeeds. Direct callers must do the same. Configuration,
allocation capacity, array pointers, and initialization metadata belong to the
lifecycle implementation and must not be modified by callers after initialization.
Lifecycle calls have one owner and are serialized; helpers that access shared
simulation state require the caller to hold `sim.lock`.
Successful pair locking must be matched by one pair unlock.

Configuration ranges are checked by `sim_init`; runtime helpers rely on the
configuration remaining unchanged. Standalone heap callers supply a valid
configuration; request checks cover the ID, timestamp, and scheduler fields
used by the heap. `request_order`, `heap_accepts`, `heap_insert`, `heap_remove`,
`pair_lock_validated`, `pair_valid`, `pair_requested`, and `sim_active` are internal
helpers for already validated objects. Callers retain the required locks between
validation and use. `heap_insert` also requires a successful insertion preflight,
and `heap_remove` requires a nonempty heap. `initial_delay` receives a configuration
validated during initialization. These helpers do not repeat boundary checks.

`sim_init`, `sim_join`, `sim_destroy`, and `heap_push` return 1 for success and 0
for failure. `sim_run` uses exit-status semantics: 0 for a normal simulation stop,
1 for failure, and accepts only a successfully initialized, unrun context.
`heap_pop` returns NULL for a valid empty heap, and reports an error before also
returning NULL for an invalid heap. `sim_destroy(NULL)` and a second destruction
after successful cleanup are harmless. Cleanup progress is retained after a
failure; `sim_run` makes one bounded join retry, and CLI cleanup makes one bounded
destruction retry. The original error remains reported with exit status 1 even
if the retry recovers all resources. A direct caller may retry `sim_join` or
`sim_destroy` when its failed operation can succeed again.

Heap boundaries reject invalid sizes, NULL requests, duplicates, mixed contexts,
unused non-NULL slots, and inconsistent order before changing the queue. Pair
operations additionally verify membership, both queues, and logical ownership.
Each coder also tracks a minimal activity state: waiting, compiling, debugging,
refactoring, or the single-dongle case. Requests are accepted from the initial
waiting state or after refactoring. A grant marks compiling; successful debugging
and refactoring log writes advance those states. State-name and transition checks
supplement the ownership checks; callers still must follow the helper's intended
order and observe the phase durations.

The first detected runtime failure is preserved with its operation and code and
stops further simulation work. These checks assume readable live objects and
NUL-terminated strings; C cannot generally verify arbitrary non-NULL pointers,
freed memory, or ownership of a damaged pthread primitive.
The first-error message is retained as a pointer, so a caller-supplied diagnostic
string must also remain alive until reporting and cleanup finish.

If joining or destroying a POSIX object fails after the bounded retries, the program retains
the simulation allocation until process exit rather than risk use-after-free.
This is an explicit exceptional limit to normal full cleanup and can appear as
retained memory in a leak report. Blocked stdout can also delay the monitor.
A closed pipe can terminate the process with SIGPIPE: `signal` and `sigaction`
are absent from the exercise's authorized function list. Valid initialized
mutexes and correct lock ownership remain caller requirements; recovery from
arbitrary memory or pthread-object corruption is not promised.

## Resources

- [Official 42 Norminette](https://github.com/42school/norminette): checker and Norm documents.
- [ryo_manba (Qiita)](https://qiita.com/ryo_manba/items/e48faf2ba84f9e5d31c8):
  "[C言語] pthread/mutexを使った並列処理", an introductory reference on
  POSIX threads, mutexes, and shared-data access.
- [Codexion Visualizer](https://codexion-visualizer.sacha-dev.me/): an external
  visualization resource for Codexion.
- 鈴木健一 (author), [よくわかる オペレーティングシステム](https://www.morikita.co.jp/books/mid/081901),
  森北出版, 2026: a reference on operating systems, process management, and
  synchronization.
- 大槻兼資 (author), 秋葉拓哉 (supervisor),
  [問題解決力を鍛える！アルゴリズムとデータ構造](https://www.kspub.co.jp/book/detail/5128442.html),
  講談社サイエンティフィク, 2020: a reference on algorithm analysis, queues,
  and heaps.

**AI use:** Codex wrote
the Makefile, this README, and the defensive API checks. During development, Codex
generated separate verification tools, heap tests, a fault-injection runner, and
learning and safety guides. AI assistance was used for source reviews, local compilation, test
execution, and documentation revisions. 

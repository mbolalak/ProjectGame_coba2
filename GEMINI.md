# CoinCollector_HananVictor — Project Context & Guidelines

## 1. Project Overview
- **Project**: CoinCollector_HananVictor (PTS Pemrograman Game Dev)
- **Engine**: Unity 6 (6000.5.3f1), Universal Render Pipeline (URP 2D)
- **Target Platform**: Standalone Windows 64-bit

## 2. MCP (Model Context Protocol) Integration
- **Package**: `com.coplaydev.unity-mcp` (MCP for Unity)
- **Bridge Window**: In Unity Editor, press `Ctrl + Shift + M` or navigate to `Window > MCP for Unity`.
- **MCP Server**: FastMCP stdio server (`mcp-for-unity`) installed via `uv`.
- **Capabilities**:
  - Inspect scene hierarchy, active GameObjects, and components.
  - Create and modify GameObjects, components, and prefabs.
  - Control Unity Play Mode (Play, Pause, Stop) for automated testing.
  - Query console logs, warnings, and compilation errors.

## 3. Core Architecture & Features
- **Game Management**: `Assets/Scripts/GameManager.cs`
- **Player Controller**: `Assets/Scripts/PlayerMovement.cs`
- **OOP Implementations**:
  - **Abstraction**: `IDamageable.cs`
  - **Inheritance**: Base `Enemy.cs` inherited by specialized enemies.
  - **Polymorphism**: Virtual/override methods (e.g. `Serang()`).
- **State Machine**: `Assets/Scripts/StateZombie.cs` (`IDLE`, `PATROL`, `CHASE`, `ATTACK`).
- **Events & Delegates**:
  - `BelajarDelegate.cs`
  - `PemancarEvent.cs` (emits jump/space event)
  - `PenerimaEvent.cs` (listens and responds on Player)

## 4. Coding Standards
- Use Unity standard conventions: PascalCase for public members/methods, camelCase for local variables and private fields with `_` prefix or camelCase.
- Expose variables to Inspector using `[SerializeField] private Type varName;` instead of `public`.
- Avoid heavy operations (e.g., `GetComponent`, `Find`, `FindObjectOfType`) inside `Update()` or `FixedUpdate()`. Cache references in `Awake()` or `Start()`.
- Use event-driven programming and delegate subscriptions, ensuring unsubscribing in `OnDisable()` or `OnDestroy()`.

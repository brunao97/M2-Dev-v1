---
trigger: always_on
---

# Metin2 Network Communication (Packets)

This document describes the standard procedure for implementing new network packets for communication between the Game Server and the Binary Client.

## Summary of Packet Communication

### 1. Game -> Client (GC)
Used when the server needs to send information to the client.

#### Server-Side (C++)
1.  **Headers and Structs**:
    -   File: `m2_source/Server/common/packet.h` (or similar shared packet header)
    -   Define a new header: `HEADER_GC_MY_PACKET = 123,`
    -   Define the packet structure:
        ```cpp
        typedef struct packet_my_packet {
            BYTE bHeader;
            int  value1;
            long value2;
        } TPacketGCMyPacket;
        ```
2.  **Sending Logic**:
    -   File: `m2_source/Server/game/src/char.h` / `char.cpp`
    -   Add sending function: `void SendMyPacket(int v1, long v2);`
    -   Implementation:
        ```cpp
        void CHARACTER::SendMyPacket(int v1, long v2) {
            if (!GetDesc()) return;
            TPacketGCMyPacket p;
            p.bHeader = HEADER_GC_MY_PACKET;
            p.value1 = v1;
            p.value2 = v2;
            GetDesc()->Packet(&p, sizeof(p));
        }
        ```

#### Client-Side (C++)
1.  **Headers and Structs**:
    -   File: `m2dev-client-src/UserInterface/Packet.h`
    -   Define same header and struct as server (must match exactly).
2.  **Packet Registration**:
    -   File: `m2dev-client-src/UserInterface/PythonNetworkStream.cpp`
    -   Add to header map (usually in `CMainPacketHeaderMap` setup):
        ```cpp
        Set(HEADER_GC_MY_PACKET, CNetworkPacketHeaderMap::TPacketType(sizeof(TPacketGCMyPacket), STATIC_SIZE_PACKET));
        ```
3.  **Handling the Packet**:
    -   File: `m2dev-client-src/UserInterface/PythonNetworkStreamPhaseGame.cpp`
    -   Add to `SetGamePhase` switch: `case HEADER_GC_MY_PACKET: ret = RecvMyPacket(); break;`
4.  **Receiving Implementation**:
    -   File: `m2dev-client-src/UserInterface/PythonNetworkStream.h` / `.cpp`
    -   `bool RecvMyPacket();`
    -   Implementation:
        ```cpp
        bool CPythonNetworkStream::RecvMyPacket() {
            TPacketGCMyPacket p;
            if (!Recv(sizeof(p), &p)) return false;
            // Forward to Python
            PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "BINARY_OnReceiveMyPacket", Py_BuildValue("(il)", p.value1, p.value2));
            return true;
        }
        ```

#### Client-Side (Python)
-   File: `assets/root/game.py`
-   Implement the callback:
    ```python
    def BINARY_OnReceiveMyPacket(self, value1, value2):
        # Handle logic here
    ```

---

### 2. Client -> Game (CG)
Used when the client needs to send information/actions to the server.

#### Client-Side (C++)
1.  **Headers and Structs**:
    -   File: `m2dev-client-src/UserInterface/Packet.h`
    -   Define a new header: `HEADER_CG_MY_ACTION = 124,`
    -   Define struct: `typedef struct command_my_action { BYTE bHeader; int value; } TPacketCGMyAction;`
2.  **Exposing to Python**:
    -   File: `m2dev-client-src/UserInterface/PythonNetworkStreamModule.cpp`
    -   Implement module function (wrapper):
        ```cpp
        PyObject* netSendMyAction(PyObject* poSelf, PyObject* poArgs) {
            int iValue;
            if (!PyArg_ParseTuple(poArgs, "i", &iValue)) return Py_BuildException();
            CPythonNetworkStream& rns = CPythonNetworkStream::Instance();
            rns.SendMyAction(iValue);
            return Py_BuildNone();
        }
        ```
    -   Register in `s_methods`.
3.  **Sending Implementation**:
    -   File: `m2dev-client-src/UserInterface/PythonNetworkStream.h` / `.cpp`
    -   `bool SendMyAction(int value);`
    -   Implementation:
        ```cpp
        bool CPythonNetworkStream::SendMyAction(int value) {
            TPacketCGMyAction p;
            p.bHeader = HEADER_CG_MY_ACTION;
            p.value = value;
            if (!Send(sizeof(p), &p)) return false;
            return SendSequence(); // Crucial for security/sync
        }
        ```

#### Server-Side (C++)
1.  **Headers and Structs**:
    -   File: `m2_source/Server/common/packet.h`
    -   Define same header and struct.
2.  **Packet Recognition**:
    -   File: `m2_source/Server/game/src/packet_info.cpp`
    -   Register in `CPacketInfoCG`: `Set(HEADER_CG_MY_ACTION, sizeof(TPacketCGMyAction), "MyAction", true);` (true for sequence check).
3.  **Dispatching**:
    -   File: `m2_source/Server/game/src/input_main.cpp`
    -   Add to `CInputMain::Analyze` switch: `case HEADER_CG_MY_ACTION: MyAction(ch, c_pData); break;`
4.  **Processing Implementation**:
    -   File: `m2_source/Server/game/src/input.h` / `input_main.cpp`
    -   `void MyAction(LPCHARACTER ch, const char* c_pData);`
    -   Implementation:
        ```cpp
        void CInputMain::MyAction(LPCHARACTER ch, const char* c_pData) {
            TPacketCGMyAction* p = (TPacketCGMyAction*)c_pData;
            // ch->DoSomething(p->value);
        }
        ```

---

## Security and Best Practices
-   **Static vs Dynamic**: Most packets are `STATIC_SIZE_PACKET`. For strings or variable data, use dynamic headers and send length first.
-   **Sequence Check**: Always use `SendSequence()` on `CG` packets to prevent simple packet injection/replay.
-   **Validation**: Always validate data on the server side (e.g., check distances, ownership, cooldowns).
-   **Packet.h Sync**: Keep `common/packet.h` (Server) and `UserInterface/Packet.h` (Client) in sync. Any mismatch in struct size or header ID will cause a "Packet Error" and disconnect.

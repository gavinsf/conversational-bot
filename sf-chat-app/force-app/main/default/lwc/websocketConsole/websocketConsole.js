import { LightningElement } from 'lwc';

const WS_URL = 'wss://rerun-paternity-sauna.ngrok-free.dev/api/ws/'; // TODO: Enter correct URL

let nextId = 0;

export default class WebsocketConsole extends LightningElement {
    log = [];
    socket;
    session_id;
    status = 'Disconnected';
    draftMessage = '';

    connectedCallback() {
        this.connect();
    }

    disconnectedCallback() {
        if (this.socket) {
            this.socket.close();
        }
    }
    connect() {
        this.socket = new WebSocket(WS_URL);

        this.socket.onopen = () => {
            this.status = 'Connected';
        }

        this.socket.onclose = () => {
            this.status = 'Disconnected';
        }

        this.socket.onmessage = (event) => {
            this.logMessage(`Received: ${event.data}`)
        }

        this.socket.onerror = (error) => {
            this.connectionStatus = 'Error';
            // eslint-disable-next-line no-console
            console.error('WebSocket error', error);
        };
    }

    handleSend() {
        if (!this.draftMessage || this.socket.readyState !== WebSocket.OPEN) {
            return;
        }

        this.socket.send(this.draftMessage);
        this.logMessage(`Sent: ${this.draftMessage}`)
        this.draftMessage = '';
    }

    logMessage(text) {
        this.log = [...this.log, { id: nextId++, text }];
    }

    handleInputChange(event) {
        this.draftMessage = event.target.value;
    }

    handleKeyUp(event) {
        if (event.key == 'Enter') {
            this.handleSend();
        }
    }

}
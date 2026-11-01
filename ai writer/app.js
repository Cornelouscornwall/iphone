const connectionButton = document.getElementById('toggleConnection');
const disconnectButton = document.getElementById('disconnectBtn');
const saveButton = document.getElementById('saveSettings');
const statusBadge = document.getElementById('statusBadge');
const regionLabel = document.getElementById('regionLabel');
const ipLabel = document.getElementById('ipLabel');
const speedLabel = document.getElementById('speedLabel');

const serverSelect = document.getElementById('serverSelect');
const protocolSelect = document.getElementById('protocolSelect');
const usernameInput = document.getElementById('usernameInput');
const passwordInput = document.getElementById('passwordInput');

const state = {
  connected: false,
  region: 'United States',
  ip: '192.168.0.20',
  speed: 'Fast lane ready'
};

const latencyByRegion = {
  'US East': '18ms',
  'US West': '22ms',
  Europe: '31ms',
  Asia: '44ms'
};

function setConnectionState(connected) {
  state.connected = connected;
  statusBadge.textContent = connected ? 'Online' : 'Offline';
  statusBadge.classList.toggle('online', connected);
  statusBadge.classList.toggle('offline', !connected);
  connectionButton.textContent = connected ? 'Disconnect' : 'Connect';
}

function applySavedSettings() {
  const selectedRegion = serverSelect.value;
  state.region = selectedRegion;
  regionLabel.textContent = selectedRegion;

  const protocol = protocolSelect.value;
  const username = usernameInput.value.trim() || 'student-user';
  const password = passwordInput.value.trim() || 'securepass';

  if (state.connected) {
    speedLabel.textContent = `${protocol} • ${latencyByRegion[selectedRegion] || '24ms'} ping`;
    ipLabel.textContent = `10.8.${Math.floor(Math.random() * 9) + 1}.${Math.floor(Math.random() * 100) + 10}`;
  }

  console.log('Saved settings:', { selectedRegion, protocol, username, password });
}

connectionButton.addEventListener('click', () => {
  const willConnect = !state.connected;
  setConnectionState(willConnect);

  if (willConnect) {
    const selectedRegion = serverSelect.value;
    const protocol = protocolSelect.value;
    regionLabel.textContent = selectedRegion;
    ipLabel.textContent = `10.8.${Math.floor(Math.random() * 9) + 1}.${Math.floor(Math.random() * 100) + 10}`;
    speedLabel.textContent = `${protocol} • ${latencyByRegion[selectedRegion] || '24ms'} ping`;
    console.log('Connected via', protocol, 'to', selectedRegion);
  } else {
    ipLabel.textContent = '192.168.0.20';
    speedLabel.textContent = 'Fast lane ready';
    console.log('Disconnected');
  }
});

disconnectButton.addEventListener('click', () => {
  setConnectionState(false);
  ipLabel.textContent = '192.168.0.20';
  speedLabel.textContent = 'Fast lane ready';
});

saveButton.addEventListener('click', () => {
  applySavedSettings();
  if (state.connected) {
    speedLabel.textContent = `${protocolSelect.value} • ${latencyByRegion[serverSelect.value] || '24ms'} ping`;
  }
});

setConnectionState(false);
applySavedSettings();

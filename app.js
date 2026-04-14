const STORAGE_KEY = 'notes-app-data';

let notes = [];
let activeId = null;
let saveTimer = null;

// ── DOM refs ──────────────────────────────────────────────
const newNoteBtn    = document.getElementById('new-note-btn');
const searchInput   = document.getElementById('search');
const notesList     = document.getElementById('notes-list');
const emptyState    = document.getElementById('empty-state');
const noteEditor    = document.getElementById('note-editor');
const noteTitle     = document.getElementById('note-title');
const noteContent   = document.getElementById('note-content');
const deleteNoteBtn = document.getElementById('delete-note-btn');
const lastSaved     = document.getElementById('last-saved');

// ── Storage ───────────────────────────────────────────────
function load() {
  try {
    notes = JSON.parse(localStorage.getItem(STORAGE_KEY)) || [];
  } catch {
    notes = [];
  }
}

function save() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(notes));
}

// ── Helpers ───────────────────────────────────────────────
function generateId() {
  return Date.now().toString(36) + Math.random().toString(36).slice(2);
}

function formatDate(ts) {
  const d = new Date(ts);
  const now = new Date();
  const diff = now - d;
  if (diff < 60_000)  return 'Just now';
  if (diff < 3_600_000) return `${Math.floor(diff / 60_000)}m ago`;
  if (diff < 86_400_000) return `${Math.floor(diff / 3_600_000)}h ago`;
  return d.toLocaleDateString(undefined, { month: 'short', day: 'numeric' });
}

function getNote(id) {
  return notes.find(n => n.id === id);
}

// ── Render ────────────────────────────────────────────────
function renderList(filter = '') {
  const term = filter.trim().toLowerCase();
  const filtered = term
    ? notes.filter(n =>
        n.title.toLowerCase().includes(term) ||
        n.content.toLowerCase().includes(term))
    : notes;

  // Sort newest first
  const sorted = [...filtered].sort((a, b) => b.updatedAt - a.updatedAt);

  notesList.innerHTML = '';
  sorted.forEach(note => {
    const li = document.createElement('li');
    li.className = 'note-item' + (note.id === activeId ? ' active' : '');
    li.dataset.id = note.id;

    const preview = note.content.replace(/\n/g, ' ').slice(0, 60) || 'No content';

    li.innerHTML = `
      <div class="note-item-title">${escapeHtml(note.title) || 'Untitled'}</div>
      <div class="note-item-preview">${escapeHtml(preview)}</div>
      <div class="note-item-date">${formatDate(note.updatedAt)}</div>
    `;

    li.addEventListener('click', () => openNote(note.id));
    notesList.appendChild(li);
  });
}

function escapeHtml(str) {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function openNote(id) {
  activeId = id;
  const note = getNote(id);
  if (!note) return;

  noteTitle.value   = note.title;
  noteContent.value = note.content;
  lastSaved.textContent = `Last saved ${formatDate(note.updatedAt)}`;

  emptyState.style.display = 'none';
  noteEditor.classList.remove('hidden');

  renderList(searchInput.value);
  noteTitle.focus();
}

function closeEditor() {
  activeId = null;
  emptyState.style.display = '';
  noteEditor.classList.add('hidden');
  renderList(searchInput.value);
}

// ── Actions ───────────────────────────────────────────────
function createNote() {
  const note = {
    id:        generateId(),
    title:     '',
    content:   '',
    createdAt: Date.now(),
    updatedAt: Date.now(),
  };
  notes.unshift(note);
  save();
  renderList(searchInput.value);
  openNote(note.id);
}

function deleteNote() {
  if (!activeId) return;
  notes = notes.filter(n => n.id !== activeId);
  save();
  closeEditor();
}

function autosave() {
  if (!activeId) return;
  const note = getNote(activeId);
  if (!note) return;

  note.title     = noteTitle.value;
  note.content   = noteContent.value;
  note.updatedAt = Date.now();
  save();

  lastSaved.textContent = 'Saved';
  renderList(searchInput.value);
}

function scheduleAutosave() {
  clearTimeout(saveTimer);
  saveTimer = setTimeout(autosave, 600);
}

// ── Event listeners ───────────────────────────────────────
newNoteBtn.addEventListener('click', createNote);
deleteNoteBtn.addEventListener('click', deleteNote);

noteTitle.addEventListener('input', scheduleAutosave);
noteContent.addEventListener('input', scheduleAutosave);

searchInput.addEventListener('input', () => renderList(searchInput.value));

// Keyboard shortcut: Ctrl/Cmd + N → new note
document.addEventListener('keydown', e => {
  if ((e.ctrlKey || e.metaKey) && e.key === 'n') {
    e.preventDefault();
    createNote();
  }
});

// ── Init ──────────────────────────────────────────────────
load();
renderList();
if (notes.length > 0) {
  openNote(notes[0].id);
}

const resultEl     = document.getElementById('result');
const expressionEl = document.getElementById('expression');

let currentValue  = '0';
let storedValue   = null;
let pendingOp     = null;
let justEvaluated = false;

// ── Display ───────────────────────────────────────────────────────────────────

function updateDisplay(expr = '') {
  const display = currentValue.length > 12
    ? parseFloat(currentValue).toExponential(6)
    : currentValue;

  resultEl.textContent = display;
  resultEl.classList.toggle('error', currentValue === 'Error');
  expressionEl.textContent = expr;
}

function buildExpression() {
  if (storedValue === null) return '';
  const opSymbol = { '+': '+', '-': '−', '*': '×', '/': '÷' }[pendingOp] ?? pendingOp;
  return `${storedValue} ${opSymbol}`;
}

// ── Arithmetic ────────────────────────────────────────────────────────────────

function calculate(a, op, b) {
  const x = parseFloat(a);
  const y = parseFloat(b);
  switch (op) {
    case '+': return x + y;
    case '-': return x - y;
    case '*': return x * y;
    case '/': return y === 0 ? null : x / y;
    default:  return x;
  }
}

function formatResult(n) {
  if (n === null) return 'Error';
  // Avoid floating-point noise (e.g. 0.1 + 0.2)
  const s = parseFloat(n.toPrecision(12)).toString();
  return s;
}

// ── Actions ───────────────────────────────────────────────────────────────────

function handleDigit(digit) {
  if (justEvaluated) {
    currentValue  = digit;
    justEvaluated = false;
  } else if (currentValue === '0' && digit !== '.') {
    currentValue = digit;
  } else if (currentValue.length < 16) {
    currentValue += digit;
  }
  updateDisplay(buildExpression());
}

function handleDecimal() {
  if (justEvaluated) {
    currentValue  = '0.';
    justEvaluated = false;
  } else if (!currentValue.includes('.')) {
    currentValue += '.';
  }
  updateDisplay(buildExpression());
}

function handleOperator(op) {
  if (currentValue === 'Error') return;

  // Chain: evaluate pending op before storing new one
  if (storedValue !== null && !justEvaluated) {
    const res = calculate(storedValue, pendingOp, currentValue);
    currentValue = formatResult(res);
    if (currentValue === 'Error') { updateDisplay(); return; }
  }

  storedValue   = currentValue;
  pendingOp     = op;
  justEvaluated = false;

  // Highlight active operator button
  document.querySelectorAll('.btn-operator').forEach(b => b.classList.remove('active'));
  document.querySelector(`[data-value="${op}"]`)?.classList.add('active');

  updateDisplay(`${storedValue} ${{ '+': '+', '-': '−', '*': '×', '/': '÷' }[op]}`);
  justEvaluated = true; // next digit starts fresh entry
}

function handleEquals() {
  if (storedValue === null || pendingOp === null || currentValue === 'Error') return;

  const expr = `${storedValue} ${{ '+': '+', '-': '−', '*': '×', '/': '÷' }[pendingOp]} ${currentValue} =`;
  const res  = calculate(storedValue, pendingOp, currentValue);

  currentValue  = formatResult(res);
  storedValue   = null;
  pendingOp     = null;
  justEvaluated = true;

  document.querySelectorAll('.btn-operator').forEach(b => b.classList.remove('active'));
  updateDisplay(expr);
}

function handleClear() {
  currentValue  = '0';
  storedValue   = null;
  pendingOp     = null;
  justEvaluated = false;
  document.querySelectorAll('.btn-operator').forEach(b => b.classList.remove('active'));
  updateDisplay();
}

function handleSign() {
  if (currentValue === '0' || currentValue === 'Error') return;
  currentValue = currentValue.startsWith('-')
    ? currentValue.slice(1)
    : '-' + currentValue;
  updateDisplay(buildExpression());
}

function handlePercent() {
  if (currentValue === 'Error') return;
  currentValue = formatResult(parseFloat(currentValue) / 100);
  updateDisplay(buildExpression());
}

// ── Event wiring ──────────────────────────────────────────────────────────────

document.querySelector('.buttons').addEventListener('click', e => {
  const btn = e.target.closest('.btn');
  if (!btn) return;

  const { action, value } = btn.dataset;
  switch (action) {
    case 'digit':    handleDigit(value);    break;
    case 'decimal':  handleDecimal();       break;
    case 'operator': handleOperator(value); break;
    case 'equals':   handleEquals();        break;
    case 'clear':    handleClear();         break;
    case 'sign':     handleSign();          break;
    case 'percent':  handlePercent();       break;
  }
});

document.addEventListener('keydown', e => {
  if (e.key >= '0' && e.key <= '9') { handleDigit(e.key); return; }
  switch (e.key) {
    case '.': case ',':   handleDecimal();         break;
    case '+':             handleOperator('+');     break;
    case '-':             handleOperator('-');     break;
    case '*':             handleOperator('*');     break;
    case '/': e.preventDefault(); handleOperator('/'); break;
    case 'Enter': case '=': handleEquals();        break;
    case 'Escape':        handleClear();           break;
    case 'Backspace':
      if (!justEvaluated && currentValue.length > 1) {
        currentValue = currentValue.slice(0, -1);
      } else {
        currentValue = '0';
      }
      updateDisplay(buildExpression());
      break;
  }
});

// ── Init ──────────────────────────────────────────────────────────────────────
updateDisplay();

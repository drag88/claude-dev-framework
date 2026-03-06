# Accessibility Patterns

Focus management, ARIA labels, and accessibility best practices for React.

---

## Focus Management

```tsx
function Modal({ isOpen, onClose, children }: ModalProps) {
  const modalRef = useRef<HTMLDivElement>(null);
  const previousFocusRef = useRef<HTMLElement | null>(null);

  useEffect(() => {
    if (isOpen) {
      // Store previous focus
      previousFocusRef.current = document.activeElement as HTMLElement;
      // Focus modal
      modalRef.current?.focus();
    } else {
      // Restore focus
      previousFocusRef.current?.focus();
    }
  }, [isOpen]);

  // Trap focus within modal
  const handleKeyDown = (e: KeyboardEvent) => {
    if (e.key === 'Escape') {
      onClose();
    }
    if (e.key === 'Tab') {
      // Trap focus logic
    }
  };

  if (!isOpen) return null;

  return (
    <div
      ref={modalRef}
      role="dialog"
      aria-modal="true"
      tabIndex={-1}
      onKeyDown={handleKeyDown}
    >
      {children}
    </div>
  );
}
```

---

## ARIA Labels

```tsx
// Button with loading state
<button
  aria-busy={isLoading}
  aria-disabled={isLoading}
  disabled={isLoading}
>
  {isLoading ? <Spinner aria-hidden /> : null}
  <span className={isLoading ? 'sr-only' : ''}>Submit</span>
  {isLoading && <span aria-live="polite">Loading...</span>}
</button>

// Form field with error
<div>
  <label htmlFor="email">Email</label>
  <input
    id="email"
    type="email"
    aria-invalid={!!error}
    aria-describedby={error ? 'email-error' : undefined}
  />
  {error && (
    <span id="email-error" role="alert">
      {error}
    </span>
  )}
</div>

// Navigation
<nav aria-label="Main navigation">
  <ul role="menubar">
    <li role="none">
      <a role="menuitem" href="/">Home</a>
    </li>
  </ul>
</nav>
```

---

## Skip Links

```tsx
function SkipLinks() {
  return (
    <div className="skip-links">
      <a href="#main-content" className="sr-only focus:not-sr-only">
        Skip to main content
      </a>
      <a href="#navigation" className="sr-only focus:not-sr-only">
        Skip to navigation
      </a>
    </div>
  );
}
```

# Animation Patterns (Framer Motion)

React animation patterns using Framer Motion.

---

## Fade In/Out

```tsx
import { motion, AnimatePresence } from 'framer-motion';

function FadeIn({ children }: { children: ReactNode }) {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.2 }}
    >
      {children}
    </motion.div>
  );
}
```

---

## List Animations

```tsx
function AnimatedList({ items }: { items: Item[] }) {
  return (
    <ul>
      <AnimatePresence>
        {items.map(item => (
          <motion.li
            key={item.id}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: 20 }}
            layout
          >
            {item.name}
          </motion.li>
        ))}
      </AnimatePresence>
    </ul>
  );
}
```

---

## Shared Layout Animation

```tsx
function ExpandableCard({ item }: { item: Item }) {
  const [isExpanded, setIsExpanded] = useState(false);

  return (
    <motion.div layout onClick={() => setIsExpanded(!isExpanded)}>
      <motion.h2 layout="position">{item.title}</motion.h2>
      <AnimatePresence>
        {isExpanded && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
          >
            {item.description}
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
}
```

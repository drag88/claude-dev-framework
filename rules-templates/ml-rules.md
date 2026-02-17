# ML / Data Science Rules Template

> Template for generating rules in ML/Data Science projects.

## Architecture Additions

### Data Flow
```
raw data → ingestion → feature engineering → training → evaluation → serving
   ↓           ↓              ↓                ↓           ↓          ↓
[source]   [staging/]    [features/]      [models/]   [metrics/]  [api/]
```

### Environment Matrix
| Environment | Purpose | GPU | Data |
|-------------|---------|-----|------|
| Local | Dev + debugging | Optional | Sample/synthetic |
| GPU Cluster | Training | Yes | Full dataset |
| Staging | Validation | Optional | Production mirror |
| Serving | Inference | [GPU/CPU] | Live requests |

## Experiment Tracking (`experiment-tracking.md`)

### Naming Convention
- Experiment: `[model_type]-[dataset]-[date]-[short_description]`
- Run: `[experiment_name]-v[N]` or auto-generated
- Artifacts: `[experiment]/[run]/[artifact_type]/`

### Required Logging
Every training run must log:
- All hyperparameters (learning rate, batch size, epochs, architecture)
- Dataset version or commit hash
- Random seeds (all of them — numpy, torch, python)
- Training metrics per epoch (loss, primary metric)
- Evaluation metrics on held-out set
- Environment info (GPU type, library versions)

### Integration Pattern
```python
# [MLflow / W&B / custom] — detect from imports and config
[tracker].log_params({...})
[tracker].log_metrics({...}, step=epoch)
[tracker].log_artifact(model_path)
```

## Data Contracts (`data-contracts.md`)

### Schema Expectations
- Every dataset has a schema definition in `[schemas/ or data/schemas/]`
- Schema includes: column names, types, nullability, valid ranges
- Schema validation runs before training and in serving pipeline

### Feature Definitions
| Feature | Type | Source | Transform | Version |
|---------|------|--------|-----------|---------|
| [name] | [numeric/categorical/text] | [raw column] | [transform] | [v1] |

### Data Versioning
- [DVC / Delta Lake / manual versioning — detect from project]
- Raw data is immutable — never modify in place
- Feature sets are versioned alongside model versions

## Patterns

### Experiment Configuration
```yaml
# config/experiment.yaml (Hydra / plain YAML / argparse)
model:
  type: [model_class]
  hidden_size: [N]
training:
  lr: [float]
  batch_size: [int]
  epochs: [int]
  seed: [int]
data:
  version: [tag/hash]
  split_ratio: [train/val/test]
```

### Notebook Conventions
1. First cell: imports and config (no credentials)
2. Early cells: data loading and exploration
3. Middle cells: processing and modeling
4. Final cells: results and visualization
5. Clear all outputs before committing
6. Notebooks are for exploration — production code goes in `src/`

### Reproducibility Rules
- Set ALL random seeds explicitly (numpy, torch, tensorflow, python random)
- Log exact library versions (`pip freeze` or lock file)
- Pin dependencies to exact versions in training environments
- Dataset splits are deterministic (seeded) or pre-computed
- Every result must be reproducible from logged config + data version

### Feature Engineering
- Feature transforms are pure functions (input → output, no side effects)
- Same transform code runs in training and serving (no training-serving skew)
- Feature pipelines are versioned with the model

## Critical Rules

1. **Never commit**: model artifacts (`.pt`, `.pkl`, `.h5`, `.onnx`), large datasets, checkpoints, credentials
2. **Pin versions exactly** in training environments — no `>=` or `~=`
3. **Config-driven experiments** — no hyperparameters hardcoded in training scripts
4. **No credentials in notebooks** — use environment variables or secret managers
5. **Validate data before training** — schema checks, null checks, distribution checks
6. **Log everything** — if you can't reproduce it, it didn't happen
7. **Separate concerns** — notebooks for exploration, `src/` for production code

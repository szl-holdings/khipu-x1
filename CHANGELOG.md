# Changelog

## 0.1.2 (unreleased)

### Fixed

- Validate complete package archives and bind verification to the exact bytes
  inspected, including malformed archive rejection (#22).
- Reject simulator numerical overflow before emitting success receipts (#21).
- Check installed distributions with isolated Python and verify dependency
  consistency in the canonical release gate.

Earlier releases are documented in GitHub Releases.

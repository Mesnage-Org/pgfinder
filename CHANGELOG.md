# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.3.0] - 2025-01-27

### Added

- More custom mass databases are now accepted — including those with extra columns (#306)

## [1.2.0] - 2024-03-20

### Added

- Added automatic structure consolidation for single datasets (#266)
- Parameterized column names via `config/columns.yaml` (#269 + #275)

### Changed

- Bumped minimum Python version to 3.10 (#269)
- Renamed old columns with `(consolidated)` to `(best match)` (#269)

## [1.1.1] - 2023-11-06

### Changed

- Changed cross-linking modifications to read donor-acceptor (#249)

## [1.1.0] - 2023-10-15

### Added

- Added a modification for enabling 3-1 cross-linking (#249)

### Fixed

- Removed the trailing space after bracketed modifications (#249)

## [1.0.3] - 2023-09-04

### Fixed

- Added `consolidation_ppm` to the output metadata (#224)

## [1.0.2] - 2023-09-03

### Fixed

- Fill in a couple of missing error messages for common mistakes (#216)

## [1.0.1] - 2023-09-03

### Added

- More user-friendly error messages for common mistakes (#214)

## [1.0.0] - 2023-09-02

### Fixed

- Restore `pgfinder_interactive.ipynb` to redirect users from the ELife paper

## [1.0.0-rc.3] - 2023-08-28

### Changed

- Nude glycan chains in the built-in mass libraries now contain `-` (#210)

## [1.0.0-rc.2] - 2023-08-28

### Changed

- Reorder `allowed_modifications.txt` (#209)
- Rename lactyl residues: `l → Lac` (#209)

## [1.0.0-rc.1] - 2023-08-27

Let there be peptidoglycan.

[Unreleased]: https://github.com/Mesnage-Org/pgfinder/compare/v1.3.0...HEAD
[1.3.0]: https://github.com/Mesnage-Org/pgfinder/compare/v1.2.2...v1.3.0
[1.2.0]: https://github.com/Mesnage-Org/pgfinder/compare/v1.1.1...v1.2.0
[1.1.1]: https://github.com/Mesnage-Org/pgfinder/compare/v1.1.0...v1.1.1
[1.1.0]: https://github.com/Mesnage-Org/pgfinder/compare/v1.0.3...v1.1.0
[1.0.3]: https://github.com/Mesnage-Org/pgfinder/compare/v1.0.2...v1.0.3
[1.0.2]: https://github.com/Mesnage-Org/pgfinder/compare/v1.0.1...v1.0.2
[1.0.1]: https://github.com/Mesnage-Org/pgfinder/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/Mesnage-Org/pgfinder/compare/v1.0.0-rc.3...v1.0.0
[1.0.0-rc.3]: https://github.com/Mesnage-Org/pgfinder/compare/v1.0.0-rc.2...v1.0.0-rc.3
[1.0.0-rc.2]: https://github.com/Mesnage-Org/pgfinder/compare/v1.0.0-rc.1...v1.0.0-rc.2
[1.0.0-rc.1]: https://github.com/Mesnage-Org/pgfinder/releases/tag/v1.0.0-rc.1

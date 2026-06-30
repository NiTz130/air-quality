# 📝 Changelog

Tất cả thay đổi đáng chú ý của dự án sẽ được ghi lại tại file này.

Format dựa theo [Keep a Changelog](https://keepachangelog.com/vi/1.1.0/),
dự án tuân theo [Semantic Versioning](https://semver.org/lang/vi/).

## [1.0.0] - 2024-01-15

### Added
- Dashboard real-time với 8 chỉ số môi trường (Nhiệt độ, Độ ẩm, CO₂, PM2.5, PM10, TVOC, CO, Occupancy).
- Hệ thống cảnh báo 3 mức (Bình thường / Cảnh báo / Nguy hiểm).
- Biểu đồ lịch sử dùng Recharts (10/20/50/tất cả).
- Fuzzy Logic Controller với 6 luật, 4 input (CO₂, PM2.5, Humidity, Occupancy), 1 output (Ventilation Level).
- REST API: `/api/current-data`, `/api/data-history/{count}`, `/api/alerts`, `/api/fuzzy-control`.
- FastAPI auto-generated docs tại `/docs`.
- Trang About mô tả kiến trúc và công nghệ.
- Pagination + search cho bảng dữ liệu.
- Export CSV.
- Scripts cài đặt cho Windows (`install.bat`) và Linux/Mac (`install.sh`).
- Makefile với target `install`, `dev`, `lint`, `format`, `test`.

### Security
- Không commit file `.env` (đã có trong `.gitignore`).
- CORS mặc định cho phép localhost.

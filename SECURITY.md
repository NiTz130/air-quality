# 🔒 Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | ✅ Active          |
| < 1.0   | ❌ End-of-life     |

## Reporting a Vulnerability

Nếu bạn phát hiện lỗ hổng bảo mật, **vui lòng KHÔNG tạo public issue**.

Thay vào đó, gửi email cho maintainer qua GitHub profile với:

- Mô tả chi tiết lỗ hổng
- Các bước tái hiện (PoC nếu có)
- Mức độ ảnh hưởng (data exposure, RCE, DoS, …)
- Đề xuất fix (nếu có)

Maintainer sẽ phản hồi trong vòng **7 ngày** và phối hợp fix trước khi công khai.

## Best Practices cho người dùng

- **Không commit** file `.env` chứa API key / DB password.
- Chạy backend ở chế độ development chỉ trên `127.0.0.1`.
- Khi deploy production, set `host=0.0.0.0` phía sau reverse proxy + TLS.
- Cập nhật `requirements.txt` thường xuyên (`pip-audit`).
- Giới hạn CORS trong `backend/main.py` cho domain thật.

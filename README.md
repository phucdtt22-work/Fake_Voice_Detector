# VoiceGuard - Hệ thống phát hiện giọng nói giả mạo AI

VoiceGuard là một ứng dụng web được xây dựng với Django, MongoDB, và các công nghệ AI để phát hiện và phân tích giọng nói giả mạo (deepfake voice) với độ chính xác cao.

## Tổng quan

Hệ thống sử dụng hai mô hình AI để phân tích âm thanh:
- **Mô hình Rapid**: Phân tích trong khoảng thời gian ngắn (2 giây), cung cấp kết quả nhanh chóng
- **Mô hình Deep**: Phân tích sâu hơn (60 giây/lần), độ chính xác cao hơn

Người dùng có thể tải lên các file âm thanh và nhận kết quả phân tích chi tiết về tính xác thực của giọng nói.

## Tính năng

- 🔐 **Xác thực người dùng**: Đăng nhập, đăng ký, đặt lại mật khẩu
- 📊 **Bảng điều khiển cá nhân**: Xem tổng quan về các phân tích đã thực hiện
- 🎵 **Tải lên âm thanh**: Tải lên file âm thanh để phân tích
- 🔍 **Phân tích chi tiết**: Biểu đồ trực quan hiển thị kết quả phân tích theo thời gian
- 👤 **Hồ sơ người dùng**: Cập nhật thông tin, ảnh đại diện
- 📱 **Giao diện responsive**: Tương thích với các thiết bị di động

## Công nghệ sử dụng

- **Backend**: Django, Python
- **Database**: MongoDB (với MongoEngine)
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **AI/ML**: Các mô hình phát hiện deepfake voice
- **Lưu trữ**: MongoEngine GridFS cho file âm thanh và hình ảnh

## Cài đặt

### Yêu cầu

- Python 3.8+
- MongoDB
- Các thư viện Python (xem file requirements.txt)

### Bước 1: Clone repository

```bash
git clone https://your-repository-url.git
cd FakeVoiceDetector
```

### Bước 2: Tạo và kích hoạt môi trường ảo

```bash
python -m venv venv
# Trên Windows
venv\Scripts\activate
# Trên MacOS/Linux
source venv/bin/activate
```

### Bước 3: Cài đặt các thư viện

```bash
pip install -r requirements.txt
```

### Bước 4: Cấu hình MongoDB

Đảm bảo MongoDB đang chạy và cập nhật cài đặt kết nối trong `myproject/settings.py`:

```python
MONGODB_SETTINGS = {
    'db': 'voiceguard_db',
    'host': 'localhost',
    'port': 27017,
}
```

### Bước 5: Chạy migration và khởi động server

```bash
python manage.py migrate
python manage.py runserver
```

Truy cập ứng dụng tại http://localhost:8000

## Cấu trúc dự án

- **audioapp/**: Ứng dụng chính chứa models, views, và forms
- **templates/**: Các template HTML
- **static/**: File tĩnh (CSS, JS, images)
- **media/**: Thư mục lưu trữ file người dùng tải lên
- **myproject/**: Cài đặt cấu hình Django

## Cách sử dụng

1. **Đăng ký tài khoản** hoặc đăng nhập nếu đã có tài khoản
2. **Tải lên file âm thanh** từ trang chủ hoặc trang hồ sơ
3. **Xem kết quả phân tích** chi tiết về tính xác thực của giọng nói
4. **Quản lý các phân tích** từ trang hồ sơ cá nhân

## Đóng góp

Vui lòng đọc [CONTRIBUTING.md](CONTRIBUTING.md) để biết thêm chi tiết về quy trình đóng góp.

## Giấy phép

Dự án này được cấp phép theo [MIT License](LICENSE).

## Liên hệ

Nếu có câu hỏi hoặc đề xuất, vui lòng liên hệ qua email: info@voiceguard.com
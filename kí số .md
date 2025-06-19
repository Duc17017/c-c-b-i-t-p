Mục đích của ký số
✅ Xác thực (Authentication): Chứng minh người ký thực sự là ai.

✅ Toàn vẹn (Integrity): Đảm bảo nội dung không bị thay đổi sau khi ký.

✅ Không chối bỏ (Non-repudiation): Người ký không thể phủ nhận đã ký dữ liệu.
![image](https://github.com/user-attachments/assets/cef3feb8-676c-4ba7-b5d6-e48a7d2d1696)


Nguyên lý hoạt động
Quy trình ký số thường gồm các bước:

Bên gửi (Người ký):
Tính băm (hash) của tài liệu bằng thuật toán băm như SHA-256.

Mã hóa giá trị băm bằng khóa riêng tư → tạo ra chữ ký số.

Gửi đi (dữ liệu gốc + chữ ký số).

Bên nhận (Người xác minh):
Tính giá trị băm của dữ liệu nhận được.

Giải mã chữ ký số bằng khóa công khai của người gửi để lấy giá trị băm gốc.

So sánh hai giá trị băm:

Nếu giống nhau → chữ ký hợp lệ.

Nếu khác nhau → dữ liệu bị thay đổi hoặc chữ ký không hợp lệ.

![image](https://github.com/user-attachments/assets/bcca94b3-1468-4157-b4cf-5498d6239382)

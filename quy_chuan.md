# Quy chuẩn chính tả viết tài liệu

Tài liệu "Ôn tập Vật Lí" cần được viết theo quy chuẩn chính tả như sau:

## Viết văn bản

- Văn bản đúng quy tắc chính tả và ngữ pháp Việt Nam.

- Sử dụng `\dblquote{}` hoặc cặp `\textquotedblleft` và `\textquotedblright` thay cho dấu  " \" " thông thường.

- Đảm bảo kí hiệu thống nhất trong tài liệu, trong đó bao gồm tên, kiểu hoa/thường, kiểu phông, kích cỡ, ...

## Đại từ nhân xưng

Khi dùng ngôi thứ nhất mà không chỉ bạn đọc, dùng "tác giả". Khi dùng ngôi thứ hai, dùng "bạn đọc". Khi dùng ngôi thứ nhất số nhiều mà bao gồm cả người đọc, dùng "chúng ta".

## Toán học

- Đáp án được đóng khung. Với văn bản và đồ thị thì đóng khung bằng `\fbox{}`, với công thức toán thì đóng khung bằng `\boxed{}`. Với đáp án trong biểu thức hay một câu, khuyến khích chỉ đóng khung phần đáp án (có thể đóng khung thêm phần xấp xỉ và dấu $\approx$ nếu cần thiết).
Ví dụ: Tỉ số giữa chu vi và đường kính của một hình tròn là $\boxed{\pi}$ (có giá trị xấp xỉ là $\boxed{\approx 3{,}14}$).
- Khi mà đáp án bị phân mảnh thì nên có một đoạn tóm tắt để vừa tổng gọn lại kết quả, vừa dễ đóng khung.
- Với bài yêu cầu chứng minh, thì viết "Qua đó, có được điều phải chứng minh." hoặc những câu mang ý nghĩa tương đương.
- Số thập phân kí hiệu bằng dấu phẩy (","). Để đảm bảo rằng không có khoảng cách giữa phần nguyên và phần thập phân, sử dụng `{,}` để viết số thập phân. Ví dụ: $9{,}34$.
- Kí hiệu tập hợp bằng kiểu liệt kê phần tử hay viết bộ số thì phân cách các phần tử bằng dấu `;`, kể cả các phần tử có phải là số hay không. Ví dụ: tập hợp $\left\{0; 1; 2\right\}$ hay bộ số $\left(a; b; c\right)$.
- Không viết dấu $\pm$ (`\pm`).
- Khi viết bản thân hàm số, dùng nguyên tên hàm $f$ thay vì $f(x)$. Khi viết giá trị của hàm số thì dùng $f(x)$ thay vì $f$.
- Khi viết tọa độ của điểm trên đồ thị, luôn viết tọa độ trong dấu ngoặc đơn, kể cả khi trong tọa độ chỉ có 1 phần tử. Ví dụ: $(1)$, $(2; 3)$, $(4; 5; 6)$.

## Đặt tên cho thành phần

Với những thành phần có `\label{}` thì đặt tên theo quy tắc sau: "Kiểu thành phần"`:`"Đường dẫn đến tệp chứ thành phần"`:`"Tên thành phần". Ví dụ: `fig:ham_so:ham_so_cap:x_2`. Viết thế này để tránh xung đột tên giữa các thành phần có cùng tên ở những tệp khác nhau.

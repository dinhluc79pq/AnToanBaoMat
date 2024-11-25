$(document).ready(function () {
    $('#form-cryption').submit(function (e) { 
        e.preventDefault()
        var formData = $(this).serialize()
        
        $.ajax({
            type: "POST",
            url: "/process_cryption",
            data: formData,
            success: function (response) {
                if(response.result) {
                    $('#result').html(response.result)
                }
                else {
                    alert('Đã xảy ra lỗi trong quá trình xử lý!')
                }
            }
        });
    });

    function ajaxForm(url, data) {
        $.ajax({
            url: url,
            type: 'POST',
            data: data,
            contentType: false,
            processData: false,
            success: function(response) {
                alert('Susscessful!')
            },
            error: function(xhr, status, error) {
                alert('Error')
            }
        })
    }

    $("#file-form").on("submit", function(e) {
        e.preventDefault();
        var formData = new FormData(this);
        formData.set('check', 'encrypt')
        ajaxForm('/upload', formData)
    });

    $('#decrypt').on('click', function(e) {
        var form = $('#file-form')[0] 
        var formData = new FormData(form);
        formData.set('check', 'decrypt')
        
        ajaxForm('/upload', formData)
    })

    const $tabButton1 = $('#tab-file');
    const $tabButton2 = $('#tab-cryption')
    const $tabPane1 = $('#tab1');
    const $tabPane2 = $('#tab2');


    // Lắng nghe sự kiện click trên mỗi tab
    $tabButton1.on('click', function() {
        console.log(123);
        
        // Loại bỏ class "active" của tất cả các tab
        $tabButton2.removeClass('active');
        $tabPane2.removeClass('active');

        // Thêm class "active" cho tab và nội dung tab được chọn
        $(this).addClass('active');
        $tabPane1.addClass('active')
    });

    $tabButton2.on('click', function() {
        console.log(123);
        
        // Loại bỏ class "active" của tất cả các tab
        $tabButton1.removeClass('active');
        $tabPane1.removeClass('active');

        // Thêm class "active" cho tab và nội dung tab được chọn
        $(this).addClass('active');
        $tabPane2.addClass('active')
    });
});
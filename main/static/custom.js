$(document).ready(function(){
    $("#loadMore").on('click',function(){
        var _currentProducts=$('.product-box').length;
        var _limit=$(this).attr('data-limit');
        var _total=$(this).attr('data-total');
        // start Ajax
        $.ajax({
            url:'/load-more-data',
            data:{
                limit:_limit,
                offset:_currentProducts,
            },
            dataType:'json',
            beforeSend:function(){
                $("#LoadMore").attr('disable',true);
                $(".load-more-icon").addClass('fa-spin');
            },
            success:function(res){
                $("#filteredProduct").append(res.data)
                $("#LoadMore").attr('disable',false);
                $(".load-more-icon").removeClass('fa-spin');
                var _totalShowing=$('.product-box').length;
                if(_totalShowing==_total){
                    $("#loadMore").remove();
                }
            }
        })      
        // End
    });
    // Product Variation
    // show price according to seleted size
    $(".choose-size").on('click',function(){
        $(".choose-size").removeClass('active');
        $(this).addClass('active'); 
        var  _price=$(this).attr('data-price');
        $(".product-price").text(_price);
    });
    // End Product variation


    // Add to cart
    $(document).on('click','.add-to-cart',function(){
        var _vm=$(this);
        var _index=_vm.attr('data-index');
        var _qty=$(".product-qty-"+_index).val();
        var _productId=$(".product-id-"+_index).val();
        var _productImage=$(".product-image-"+_index).val();
        var _productTitle=$(".product-title-"+_index).val();
        var _productPrice=$(".product-price-"+_index).text();
        // ajax
        $.ajax({
            url:'/add-to-cart',
            // method:'post',
            data:{
                'id':_productId,
                'image':_productImage,
                'qty':_qty,
                'title':_productTitle,
                'price':_productPrice
            },
            dataType:'json',
            beforeSend:function(){
                _vm.attr('disabled',true);
                
            },
            success:function(res){
                $(".cart-list").text(res.totalitem);
                _vm.attr('disabled',false);
            }
        });
        // end Ajax

    });
    
    // End Add to cart

    // Delete item from cart
    $(document).on('click','.delete-item',function(){
		var _pId=$(this).attr('data-item');
		var _vm=$(this);
		// Ajax
		$.ajax({
			url:'/delete-from-cart',
			data:{
				'id':_pId,
			},
			dataType:'json',
			beforeSend:function(){
				_vm.attr('disabled',true);
			},
			success:function(res){
				$(".cart-list").text(res.totalitems);
				_vm.attr('disabled',false);
				$("#cartList").html(res.data);
			}
		});
		// End
	});

// Update item from cart
$(document).on('click','.update-item',function(){
    var _pId=$(this).attr('data-item');
    var _pQty=$(".product-qty-"+_pId).val();
    var _vm=$(this);
    // Ajax
    $.ajax({
        url:'/update-cart',
        data:{
            'id':_pId,
            'qty':_pQty
        },
        dataType:'json',
        beforeSend:function(){
            _vm.attr('disabled',true);
        },
        success:function(res){
            // $(".cart-list").text(res.totalitems);
            _vm.attr('disabled',false);
            $("#cartList").html(res.data);
        }
    });
    // End
});
    // Activate Seleted address
    $(document).on('click','.activate-address',function(){
		var _aId=$(this).attr('data-item');
		var _vm=$(this);
		// Ajax
		$.ajax({
			url:'/delete-from-cart',
			data:{
				'id':_pId,
			},
			dataType:'json',
			beforeSend:function(){
				_vm.attr('disabled',true);
			},
			success:function(res){
				$(".cart-list").text(res.totalitems);
				_vm.attr('disabled',false);
				$("#cartList").html(res.data);
			}
		});
		// End
	});


});

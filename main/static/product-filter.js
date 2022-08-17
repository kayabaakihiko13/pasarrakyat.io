$(document).ready(function(){
    $(".ajaxLoader").hide();
    $(".filter-checkbox").on('click',function(){
        var _filterObj={};
        $(".filter-checkbox").each(function(_index,_ele){
            var _filterVal=$(this).val();
            var _filterKey=$(this).data('filter');
            _filterObj[_filterKey]=Array.from(document.querySelectorAll('input[data-filter='+_filterKey+']:checked')).map(function(el){
                return el.value;
           });
        });
        // run Ajax
        $.ajax({
            url:'/filter-data',
            // method:'post',
            data:_filterObj,
            dataType:'json',
            beforeSend:function(){
                $(".ajaxLoader").show();
                
            },
            success:function(res){
                console.log(res);
                $("#filteredProduct").html(res.data);
                $(".ajaxLoader").hide();
            }
        });
    });
});
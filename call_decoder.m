%%
function result=call_decoder(py_path, config_path, data)
    if nargin < 2
        config_path = '';
    end
    if nargin < 3
        data = py.None;
    end
    % 添加python的搜索路径
    P = py.sys.path; 
    if count(P, py_path) == 0
        insert(P,int32(0), py_path);
    end
    % 调用 Python 函数
    result = py.decode.main(config_path, data);
    result = int64(result);
end


"""
错误处理器
"""
from flask import jsonify
from werkzeug.exceptions import HTTPException
from flask_jwt_extended.exceptions import JWTExtendedException


def register_error_handlers(app):
    """注册错误处理器"""
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': '资源不存在'}), 404
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'error': '请求参数错误'}), 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({'error': '未授权访问'}), 401
    
    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({'error': '禁止访问'}), 403
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({'error': '请求方法不允许'}), 405
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': '服务器内部错误'}), 500
    
    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        return jsonify({'error': error.description}), error.code
    
    @app.errorhandler(JWTExtendedException)
    def handle_jwt_exceptions(error):
        return jsonify({'error': 'JWT令牌错误'}), 401
    
    @app.errorhandler(Exception)
    def handle_general_exception(error):
        app.logger.error(f'未处理的异常: {str(error)}')
        return jsonify({'error': '服务器错误，请稍后重试'}), 500
#block api
from flask_restful import Resource
from backend.extensions import api
from backend.block import operations

@api.route('/api/blocks')
class BlockListApi(Resource):
    def get(self):
        res = operations.get_block_list(1, 5)
        return {"len": len(res)}

@api.route('/api/blocks/<int:blockid>')
class BlockApi(Resource):
    def get(self, blockid):
        return {blockid:"value"}

#root@localhost: g7c2*b)U<&NT
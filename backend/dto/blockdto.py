class BlockDTO(object):
    @classmethod
    def convert(cls, http_block_dict):
        new_dict = dict()
        new_dict["blockid"] = http_block_dict.get("blockID")
        new_dict["number"] = http_block_dict.get("block_header").get("raw_data").get("number")
        new_dict["witness_address"] = http_block_dict.get("block_header").get("raw_data").get("witness_address")
        new_dict["parenthash"] = http_block_dict.get("block_header").get("raw_data").get("parentHash")
        new_dict["version"] = http_block_dict.get("block_header").get("raw_data").get("version")
        new_dict["timestamp"] = int(http_block_dict.get("block_header").get("raw_data").get("timestamp")) / 1000
        return new_dict
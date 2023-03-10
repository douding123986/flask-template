import re


class Config:
    @staticmethod
    def port():
        regex1 = r'^(GigabitEthernet\d+/0/\d+|XGigabitEthernet\d+/0/\d+|Ten-GigabitEthernet\d+/0/\d+|Eth-Trunk\d+|'
        regex2 = r'gei-0/\d+/0/\d+|xgei-0/\d+/0/\d+|gei_\d+/\d+|xgei_\d+/\d+|smartgroup\d+)$'
        return regex1 + regex2

    @staticmethod
    def device_port():
        regex = re.sub(r'[\^$]', '', Config.port())
        regex = r'^.+:' + regex + '$'
        return regex

    @staticmethod
    def bras_full_name():
        regex = r'^(b\d-[a-z]-gdzj-[a-z]+|r\d-[a-z]-gdzj-[a-z]+|s\d-[a-z]-gdzj-[a-z]+)$'
        return regex

    @staticmethod
    def keys():
        return r'^(major|backup_[1-5])$'

    @staticmethod
    def access_info():
        regex = r'^(.+{10,20}|.+{10,20}:.+{5,15}|.+{10,20}:.+{5,15}<---->.+{10,20}:.+{5,15}{1,5})$'
        return regex

    @staticmethod
    def route_regex():
        ip = r'((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3}'
        mask = r'(((255\.){3}(255|254|252|248|240|224|192|128|0+))' + '|' + \
               r'((255\.){2}(255|254|252|248|240|224|192|128|0+)\.0)' + '|' + \
               r'((255\.)(255|254|252|248|240|224| 192|128|0+)(\.0+){2})' + '|' + \
               r'((255|254|252|248|240|224|192|128|0+)(\.0+){3}))'
        # ["掩码：255.255.255.224", "网关：58.252.218.33", "DNS(主)：120.80.88.88", "DNS(备)：221.5.88.88"]
        mask_router = '掩码[1-9]{0,1}：' + mask + '|' + '网关[1-9]{0,1}：' + ip
        dns = r'DNS\(主\)：' + ip + '|' + r'DNS\(备\)：' + ip
        regex = r'^(' + mask_router + '|' + dns + ')$'
        return regex

    @staticmethod
    def ipaddress():
        ipv4 = r'((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3}[\s]{0,1}'
        ipv4_address = ipv4 + '-' + ipv4 + '|' + ipv4
        ipv6_address = r'(([a-fA-F0-9]{1,4}:|){0,7}[::]{0,1}[a-fA-F0-9]{1,4})/\d{0,3}[\s]{0,1}'
        ip_regex = r'^(' + ipv4_address + '|' + ipv6_address + '){1,5}$'
        return ip_regex

    @staticmethod
    def vlan():
        vlan = r'[1-9]\d{1,2}|[1-3]\d{3}|40[0-9][0-4]'
        regex = r'^(' + vlan + '|' + vlan + '/' + vlan + '|' + vlan + '-' + vlan + ')$'
        return regex

    @staticmethod
    def places():
        return ['霞山', '赤坎', '开发区', '坡头', '吴川', '遂溪', '廉江', '徐闻', '雷州']

    @staticmethod
    def manufactures():
        return ['华为', '中兴', '华三', '思科', '烽火']

    @staticmethod
    def level():
        return ['汇聚以上设备', '接入交换机', '一级交换机']

    @staticmethod
    def department():
        return ['transmission', 'core', 'delivery_center', 'other']

    @staticmethod
    def types():
        return ['Bras', 'Switch', 'CR']

    @staticmethod
    def network_levels():
        return ['GD_MAN_BRAS', 'GD_MAN_CORE', 'GD_MAN_SW']

    @staticmethod
    def port_bandwidths():
        return ['1G', '10G']

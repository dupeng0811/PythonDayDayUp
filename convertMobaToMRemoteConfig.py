import configparser
import os
import configparser
import uuid
from xml.dom import minidom
from xml.etree.ElementTree import SubElement

"""
读取配置文件信息
"""

# class ConfigParser():
#
#     config_dic = {}
#     @classmethod
#     def get_config(cls, sector, item):
#         value = None
#         try:
#             value = cls.config_dic[sector][item]
#         except KeyError:
#             cf = configparser.ConfigParser()
#             cf.read('MobaXterm.ini', encoding='gbk')  #注意setting.ini配置文件的路径
#             value = cf.get(sector, item)
#             cls.config_dic = value
#         finally:
#             return value


if __name__ == '__main__':
    # 当前文件路径
    proDir = os.path.split(os.path.realpath(__file__))[0]
    # 在当前文件路径下查找.ini文件
    configPath = os.path.join(proDir, "MobaXterm.ini")
    conf = configparser.ConfigParser()
    # 读取.ini文件
    conf.read(configPath)
    # get()函数读取section里的参数值
    # name = conf.get("section1", "name")
    # print(name)
    print(conf.sections())
    # print(conf.options('section1'))
    # print(conf.items('section1'))
    root = minidom.Document()
    xml = root.createElement('mrng:Connections')
    xml.setAttribute('xmlns:mrng', 'http://mremoteng.org')
    xml.setAttribute('EncryptionEngine', 'AES')
    xml.setAttribute('BlockCipherMode', 'GCM')
    xml.setAttribute('KdfIterations', "1000")
    xml.setAttribute('FullFileEncryption', "false")
    xml.setAttribute('Protected', "0mN3Qf5r1EszTFgOsDOKusTSMMJ4L4x7WjUV3yV54L63Cp7UZPjYtQDxOTHcaDX2CMmxqag3uexKnhXyh2FrtTDR")
    xml.setAttribute('ConfVersion', "2.6")
    xml.setAttribute('Export', "false")
    root.appendChild(xml)
    for secItem in conf.sections():
        print(secItem)
        containerChild = root.createElement('Node')
        containerChild.setAttribute('xmlns:mrng', 'http://mremoteng.org')
        containerChild.setAttribute('Name', secItem)
        containerChild.setAttribute('Type', 'Container')
        containerChild.setAttribute('Id', str(uuid.uuid5(uuid.NAMESPACE_DNS, secItem)))
        # print('options:' + str(conf.options(secItem)))
        # print('items:' + str(conf.items(secItem)))
        for item in conf.items(secItem):
            name = item[0]
            addressInfo = item[1].split('@')
            ipaddress = addressInfo[0]
            username = addressInfo[1]
            print(name, addressInfo)
            itemChild = root.createElement('Node')
            itemChild.setAttribute('xmlns:mrng', 'http://mremoteng.org')
            itemChild.setAttribute('Name', name)
            itemChild.setAttribute('Type', 'Connection')
            itemChild.setAttribute('Id', str(uuid.uuid5(uuid.NAMESPACE_DNS, secItem)))
            itemChild.setAttribute('Username', username)
            itemChild.setAttribute('Hostname', ipaddress.split(':')[0])
            itemChild.setAttribute('Port', ipaddress.split(':')[1])
            itemChild.setAttribute('Protocol', 'RDP')
            containerChild.appendChild(itemChild)
        xml.appendChild(containerChild)

    xml_str = root.toprettyxml(indent="\t")

    save_path_file = "gfg.xml"

    with open(save_path_file, "w") as f:
        f.write(xml_str)

#!/usr/bin/python3
#-*- coding:utf-8-*-
def convert (octal):
        """ Verifie si l'argument estun number"""
        if isinstance(octal, str):
            octalint = int(octal)
            return octalint
        elif isinstance(octal, int):
            return octal
        else:
            raise TypeError

def verify(octal):
    """ Methode satic pour verifier l'adress"""
    try:
        value = convert(octal)
        if value >= 0 & value <= 255:
            return value
    except TypeError as e:
        print(e)

def checking_address(address):
        """Methode pour valider l'adresse"""
        address_check = [ x for x in map(verify, address)]
        return address_check

def give_mask(address):
        """Methode pour donner un mask a l'adresse"""
        try:
            fist_element = convert(address[0])
        except TypeError as err:
            print(err)
        else:
            if fist_element >= 0 and fist_element <= 126:
                mask = [255, 0, 0, 0]
                return mask
            elif fist_element >= 128 and fist_element <= 191:
                mask = [255, 255, 0, 0]
                return mask
            elif fist_element >= 192 and fist_element <= 223:
                mask = [255, 255, 255, 0]
                return mask
            else:
                mask = [240, 0, 0,0]
                return mask

def a_genarator():
    for i in range(1, 255):
        yield i


class Address(object):
    """[This class allow to create objects address ipv4 and their parametters ]

    Arguments:
        object {[addresse ipv4]} -- [to initialise the address you can give the mask or this the address in his string form ]
    """
    def __init__(self, address, mask=None):
        #self.address = address
        self.good_address = checking_address(address.split("."))
        if mask is not None:
            self.mask = mask.split(".")
        else:
            if self.good_address:
                print(self.good_address)
                self.mask = give_mask(self.good_address)
            else:
                raise ValueError
        self.mask_string = ".".join(str(v) for v in self.mask)
        if self.is_network_address:
            self.address = address
        else:
            self.address = self.give_network_address
        



    def modify_address(self, index, value):
        """
           Une methode pour modifier l'addresse IP
           pour modifier il faut donner l'index de
           l'octet qu'il faut modifier
        """
        self.good_address[index] = value



    def is_network_address(self):
        """[Cheking if this address is a network address]

        Returns:
            [Boolean] -- [True or False]
        """
        zero = self.good_address.count(0)
        if zero >= 1 and self.mask_string == "255.255.0.0":
            return True
        elif zero == 1 and self.mask_string == "255.255.255.0":
            return True
        else:
            return False

    def is_class_A(self):
        """[Cheking if the class of this address is A]

        Returns:
            [Boolean] -- [True or False]
        """
        return self.mask_string == '255.0.0.0'
    
    def is_class_B(self):
        """[Cheking if the class of this address is B]

        Returns:
            [Boolean] -- [True or False]
        """
        return self.mask_string == '255.255.0.0'
    
    def is_class_C(self):
        """[Cheking if the class of this address is C]

        Returns:
            [Boolean] -- [True or False]
        """
        return self.mask_string == '255.255.255.0'

            

    def is_class_D(self):
        """[Cheking if the class of this address is D]

        Returns:
            [Boolean] -- [True or False]
        """
        return self.mask_string == '240.0.0.0'

    
    def give_network_address(self):
        """[This  methode give the network address of this address]

        Returns:
            [String] -- [it'll be like 'xxx.xxx.xxx.xxx']
        """
       
        if not self.is_network_address():
            if self.is_class_A():
                for i in range(1, 4):
                    self.good_address.pop(i)
                    self.good_address.insert(i, 0)
                return ".".join(str(v) for v in self.good_address)

            if self.is_class_B():
                for i in range(2, 4):
                    self.good_address.pop(i)
                    self.good_address.insert(i, 0)
                return ".".join(str(v) for v in self.good_address)

            if self.is_class_C():
                self.good_address.pop(3)
                self.good_address.insert(3, 0)
                return ".".join(str(v) for v in self.good_address)
        else:
            return self.address

    def broadcast_address(self):
        """[this methode give the broadcast address of this address]

        Returns:
            [String] -- [it'll be likee 'xxx.xxx.xxx.xxx']
        """
        # Firstly we need to know the indexs of all value==0 in the mask
        collect = [self.mask.index(x) for x in self.mask if int(x) == 0]
        for i in  range(collect[0], 4):
            self.good_address.pop(i)
            self.good_address.insert(i, 255)
        return ".".join(str(v) for v in self.good_address)
    
    
    def give_host_address(self):
        """[this methode gerete all host address for this address]

        Returns:
            [list] -- [contain all host network and depend about the class of the address]
        """
        #network_address is a enerator we sould transforme it into a list
        network_address = a_genarator()
        network_address = list(network_address)
        print(self.good_address)
        list_returned = []
        if self.is_class_A():
            for i in network_address:
                for j in range(1,4):
                    self.good_address.pop(j)
                    self.good_address.insert(j, i)
                    list_returned.append(".".join(str(v) for v in self.good_address))
            return list_returned

        if self.is_class_B():
            for i in network_address:
                for j in range(2,4):
                    self.good_address.pop(j)
                    self.good_address.insert(j, i)
                    list_returned.append(".".join(str(v) for v in self.good_address))
            return list_returned

        if self.is_class_C():
            for i in network_address:
                self.good_address.pop(3)
                self.good_address.insert(3, i)
                list_returned.append(".".join(str(v) for v in self.good_address))
        return list_returned
    

    def __repr__(self):
        return f'address: {self.address} \nnetwork address: {self.give_network_address()} \nmask: {self.mask_string}  \nbroadcast address: {self.broadcast_address()}'

    def __str__(self):
        return repr(self)
            

            






if __name__ == "__main__":
    addrss = Address("192.168.1.1")
    print(addrss)
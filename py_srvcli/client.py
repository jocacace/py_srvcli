import sys

from example_interfaces.srv import AddTwoInts
import rclpy
from rclpy.node import Node


class ServiceClient(Node):

    def __init__(self):
        super().__init__('service_client_async')
        self.cli = self.create_client(AddTwoInts, 'add_two_ints')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = AddTwoInts.Request()

    def send_request(self):
        self.req.a = int(sys.argv[1])
        self.req.b = int(sys.argv[2])
        self.future = self.cli.call_async(self.req)


def main(args=None):
    rclpy.init(args=args)

    service_client = ServiceClient()
    service_client.send_request()

    while rclpy.ok():
        rclpy.spin_once(service_client)
        if service_client.future.done():
            try:
                response = service_client.future.result()
            except Exception as e:
                service_client.get_logger().info(
                    'Service call failed %r' % (e,))
            else:
                service_client.get_logger().info(
                    'Result of add_two_ints: for %d + %d = %d' %
                    (service_client.req.a, service_client.req.b, response.sum))
            break

    service_client.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()